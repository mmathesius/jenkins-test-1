pipeline {
    agent {
        label '!windows'
    }

    stages {
        stage('Generate compose report and alerts') {
            steps {
                script {
                    // get status.yaml artifact from previous run
                    try {
                        copyArtifacts(projectName: currentBuild.projectName, filter: "status.yaml")
                    } catch(err) {
                        // create empty file if missing
                        sh "touch status.yaml"
                    }
                    sh "mv status.yaml status-prev.yaml"
                    sh "./scripts/compose_monitor/compose_check.py --debug --config scripts/compose_monitor/config.yaml --input status-prev.yaml"
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
