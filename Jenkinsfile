pipeline {
    agent {
        label '!windows'
    }

    stages {
        stage('Generate compose report') {
            steps {
                script {
                    sh "./scripts/last_good/report.py"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts allowEmptyArchive: true, artifacts: 'output/*', fingerprint: true
        }
    }
}
