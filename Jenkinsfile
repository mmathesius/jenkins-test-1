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

                    if (buildstatus == 'FAILED') {
		        def Message = "test message body"
		        emailext to: "mmathesi@redhat.com",
			    from: "merlinm-jenkins-test@redhat.com",
			    subject: "Jenkins build $buildname FAILED!",
			    body: Message

                        error 'Compose Failed'
                    }
                }
            }
        }

    }
}
