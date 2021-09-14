def failure_email_sender = "merlinm-jenkins-test@redhat.com"
def failure_email_recipient = "mmathesi@redhat.com"
def composeattrs = null
def buildstatus = 'UNKNOWN'

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

        stage('Wait for Compose to finish'){
            steps {
                // timeout(time: 120, unit: 'MINUTES')
                timeout(time: 90, unit: 'SECONDS') {
                    script {
                        buildstatus = 'UNKNOWN'
                        Exception caughtException = null

                        // if an error occurs, abort this stage without failing the build
                        catchError(buildResult: null, stageResult: 'ABORTED') {
                            try {
                                while( true ) {
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
                            } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
                                buildstatus = 'TIMEOUT'
                                error "Caught ${e.toString()}"
                            } catch (Throwable e) {
                                caughtException = e
                            }
                        } // catchError()

                        // if an unexpected exception occurred, go ahead and fail the build
                        if (caughtException) {
                            error caughtException.message
                        }
                    }
                } // timeout()
            }
        } // stage()

        stage('Report Compose Result') {
            steps {
                script {
                    def buildname = "unknown-build"
                    if (composeattrs) {
                        buildname = composeattrs['pungi_compose_id']
                        currentBuild.displayName = "$buildname"
                    }

		    echo "Jenkins build $buildname status = $buildstatus"

                    if (buildstatus != 'SUCCESS') {
		        def failure_subject = "Production compose $buildname status: $buildstatus!"
		        def failure_message = """Greetings.

Jenkins production compose build $buildname status is $buildstatus.

Job URL: ${BUILD_URL}"""
		        emailext to: failure_email_recipient,
			    from: failure_email_sender,
			    subject: failure_subject,
			    body: failure_message

                        error "Compose Status $buildstatus"
                    }
                }
            }
        }
    }
}
