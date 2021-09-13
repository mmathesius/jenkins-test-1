pipeline {
    agent {
        label '!windows'
    }

    triggers {
        cron('H/10 * * * *')
        upstream(upstreamProjects: "My-Pipeline/compose-report")
    }

    stages {
        stage('Build') {
            steps {
                echo "Hello"
            }
        }
    }
}
