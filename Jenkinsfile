pipeline{
    agent { label 'jenkins-slave-cloud' }
    stages{
        stage("A"){
		agent {
			docker {
				reuseNode true
				image 'python:3.7'
				args '-u root:root'
			}
		}
            steps{
                sh "pip install -r requirements-dev.txt"
                sh "./install.sh"
                sh "py.test"
            }
            post{
                always{
                    echo "========always=======tested"
                }
                success{
                    echo "========A executed successfully========"
                }
                failure{
                    echo "========A execution failed========"
                }
            }
        }
    }
    post{
        always{
            echo "========always========"
        }
        success{
            echo "========pipeline executed successfully ========"
        }
        failure{
            echo "========pipeline execution failed========"
        }
    }
}
