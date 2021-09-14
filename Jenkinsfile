def failure_email_sender = "merlinm-jenkins-test@redhat.com"
def failure_email_recipient = "mmathesi@redhat.com"
def composeattrs = null
def buildstatus = "UNKNOWN"

pipeline {
    agent {
        label '!windows'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }

        stage('Hang') {
            steps {
                // timeout(time: 120, unit: 'MINUTES') {
                timeout(time: 10, unit: 'SECONDS') {
                    script {
                        while( true ){
                            sleep 60 // seconds
                            // sh "curl --negotiate -u : -o response.json https://odcs.stream.rdu2.redhat.com/api/1/composes/$composeid"

                            composeattrs = readJSON file: 'response.json'

                            if (composeattrs['state'] == 2) { //done
                                buildstatus = 'SUCCESS'
                                return
                            } else if (composeattrs['state'] == 4) { //failed
                                buildstatus = 'FAIL'
                                return
                            }
                        }
                    }
                }
            }
        }

        stage('Report Compose result') {
            steps {
                script {
                    def buildname = "unknown-build"
                    if (composeattrs)
                        buildname = composeattrs['pungi_compose_id']
                        currentBuild.displayName = "$buildname"
                    }

		    echo "Jenkins build $buildname status = $buildstatus"

                    if (buildstatus == 'FAIL') {
		        def failure_subject = "Production compose $buildname has FAILED!"
		        def failure_message = """Greetings.

Jenkins production compose build $buildname has failed.

Job URL: ${BUILD_URL}"""
		        emailext to: failure_email_recipient,
			    from: failure_email_sender,
			    subject: failure_subject,
			    body: failure_message

                        error 'Compose Failed'
                    }
                }
            }
        }

    }
}
