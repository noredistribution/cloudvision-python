# Copyright (c) 2020 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the COPYING file.

# Acknowledge CVP events.
# Acknowledging a CVP event hides the event from the default view
#
# Examples:
# 1) Acknowledge all events:
#   $ python ack_events.py
# 2) Acknowledge all events after date:
#   $ python ack_events.py --start 2020-02-20T00:00:01.000000001Z
# 3) Acknowledge all INSUFFICIENT_PEER_LAG_REDUNDANCY events between two dates:
#   $ python ack_events.py --event-type INSUFFICIENT_PEER_LAG_REDUNDANCY \
#   --start 2020-02-20T00:00:01.000000001Z \
#   --end 2020-02-21T00:00:01.000000001Z
# 4) Acknowledge all events with INFO severity:
#   $ python ack_events.py --severity INFO
import argparse

import grpc

import arista.event.v1.event_pb2 as models
import arista.event.v1.services.gen_pb2 as messages
import arista.event.v1.services.gen_pb2_grpc as service

RPC_TIMEOUT = 30  # in seconds
SEVERITIES = ["INFO", "WARNING", "ERROR", "CRITICAL"]


def main(args):
    token = args.token_file.read().strip()
    callCreds = grpc.access_token_call_credentials(token)

    if args.cert_file:
        cert = args.cert_file.read()
        channelCreds = grpc.ssl_channel_credentials(root_certificates=cert)
    else:
        channelCreds = grpc.ssl_channel_credentials()
    connCreds = grpc.composite_channel_credentials(channelCreds, callCreds)

    get_all_req = messages.EventStreamRequest()

    if args.end and not args.start:
        raise ValueError("--start must be specified when --end is specified")

    if args.start:
        if args.start.isdigit():
            get_all_req.time.start.FromNanoseconds(int(args.start))
        else:
            get_all_req.time.start.FromJsonString(args.start)
        # set end to current time in case end is not specified
        get_all_req.time.end.GetCurrentTime()

    if args.end:
        if args.end.isdigit():
            get_all_req.time.end.FromNanoseconds(int(args.end))
        else:
            get_all_req.time.end.FromJsonString(args.end)

    event_filter = models.Event()

    if args.event_type:
        event_filter.event_type.value = args.event_type

    if args.severity:
        # enum with val 0 is always unset
        event_filter.severity = SEVERITIES.index(args.severity) + 1

    get_all_req.partial_eq_filter.append(event_filter)
    print(f"acking events that match the filter {get_all_req}")

    with grpc.secure_channel(args.server, connCreds) as channel:
        event_stub = service.EventServiceStub(channel)
        event_ack_stub = service.EventAnnotationConfigServiceStub(channel)
        for resp in event_stub.GetAll(get_all_req, timeout=RPC_TIMEOUT):
            if not resp.value.ack.ack.value:
                print(f"acking event {resp}")
                req = messages.EventAnnotationConfigSetRequest(
                    value=models.EventAnnotationConfig(
                        key=resp.value.key,
                    )
                )
                req.value.ack.value = True
                event_ack_stub.Set(req, timeout=RPC_TIMEOUT)


if __name__ == '__main__':
    ds = ("Acknowledge CVP events. "
          "Acknowledging a CVP event hides the event from the default view. "
          "Examples:\n"
          "1) Acknowledge all events:\n"
          "\tpython ack_events.py\n"
          "2) Acknowledge all events after date:\n"
          "\tpython ack_events.py --start 2020-02-20T00:00:01.000000001Z\n"
          "3) Acknowledge all INSUFFICIENT_PEER_LAG_REDUNDANCY events between "
          "two dates\n"
          "\tpython ack_events.py --event-type "
          "INSUFFICIENT_PEER_LAG_REDUNDANCY --start 2020-02-20T00:00:01.000000001Z "
          "--end 2020-02-21T00:00:01.000000001Z\n"
          "4) Acknowledge all events with INFO severity:\n"
          "\tpython ack_events.py --severity INFO")
    parser = argparse.ArgumentParser(
        description=ds,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--server',
        required=True,
        help="CloudVision server to connect to in <host>:<port> format")
    parser.add_argument('--start',
                        help=("acknowledge events after this time. "
                              "RFC3339 date string or Unix nanosecond timestamp."))
    parser.add_argument('--end',
                        help=("acknowledge events before this time. "
                              "RFC3339 date string or Unix nanosecond timestamp. "
                              "Must also provide start time argument"))
    parser.add_argument("--event-type", help="acknowledge events of this type only")
    parser.add_argument("--severity",
                        help="acknowledge events of this severity only",
                        choices=SEVERITIES)
    parser.add_argument("--token-file", required=True,
                        type=argparse.FileType('r'), help="file with access token")
    parser.add_argument("--cert-file", type=argparse.FileType('rb'),
                        help="certificate to use as root CA")
    args = parser.parse_args()
    main(args)
