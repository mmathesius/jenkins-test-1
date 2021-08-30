def failure_email_sender = "merlinm-jenkins-test@redhat.com"
def failure_email_recipient = "mmathesi@redhat.com"

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

        stage('Report Compose result') {
            steps {
                script {
                    def composeattrs = readJSON file: 'response.json'
                    def buildname = composeattrs['pungi_compose_id']
                    def buildstatus = (composeattrs['state'] == 4) ? 'FAIL' : 'SUCCESS'
                    currentBuild.displayName = "$buildname"

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
