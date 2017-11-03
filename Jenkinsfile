pipeline {
  agent any

  environment {
        GIT_NAME = "eea.progressbar"
    }

  stages {
       stage('Functional tests') {
      steps {
        parallel(

          "WWW": {
            node(label: 'docker-1.13') {
            }
          },

          "KGS": {
            node(label: 'docker-1.13') {
            }
          },

          "Plone4": {
            node(label: 'docker-1.13') {
              script {
                try {
                     checkout scm
                     sh '''ls -ltr'''
                     sh '''docker run -p 8080 -e ADDONS=eea.progressbar -e DEVELOP=src/eea.progressbar -v $(pwd):/plone/instance/src/eea.progressbar  --name=$BUILD_TAG-ft-plone4 eeacms/plone-test:4'''
                     sh '''docker port $BUILD_TAG-ft-plone4 8080/tcp > url.file;docker_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}' $BUILD_TAG-ft-plone4); sed -i -e "s/0.0.0.0/${docker_ip}/g" url.file'''
                     sh '''new_url=$(cat url.file);timeout 300  wget --retry-connrefused --tries=60 --waitretry=5 -q http://${new_url}/'''
                     sh '''new_url=$(cat url.file);casperjs test eea/progressbar/ftests/plone4/*.js --url=${new_url} --xunit=ftestsreport.xml'''
                
                }
                finally {
                  sh '''docker stop $BUILD_TAG-ft-plone4'''
                  sh '''docker rm -v $BUILD_TAG-ft-plone4'''
                }
               }
              junit 'ftestsreport.xml'
              archiveArtifacts 'screenshot1.png'

              }

            }
          )
      }
    }
    
  }
}
