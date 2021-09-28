pipeline {
    agent {
        label '!windows'
    }

    stages {
        stage('Generate compose report') {
            steps {
                script {
                    // get status.yaml artifact from previous run
                    try {
                        copyArtifacts(projectName: currentBuild.projectName, filter: "status.yaml")
                    } catch(err) {
                        // create empty file if missing
                        sh "touch status.yaml"
                    }
                    sh "mv status.yaml oldstatus.yaml"
                    sh "./scripts/compose_monitor/compose-check.py --debug --config scripts/compose_monitor/config-eln.yaml --input oldstatus.yaml"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts allowEmptyArchive: true, artifacts: 'status.yaml,output/*', fingerprint: true
        }
    }
}
