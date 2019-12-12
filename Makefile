PCOMP = protoc
PB_DIR = AerisRequester/protobuf
GEN_DIR = AerisRequester/gen
PCOMP_FLAGS = -I=$(PB_DIR) --python_out=$(GEN_DIR) --mypy_out=$(GEN_DIR)



.PHONY: clean
# re-generate python protobuf files 
proto:
	$(PCOMP) $(PCOMP_FLAGS) $(PB_DIR)/*.proto

# clean all stuff related to dist-ing these packages
clean:
	rm -rf AerisRequester.egg-info build dist

lint:
	flake8 && mypy .

