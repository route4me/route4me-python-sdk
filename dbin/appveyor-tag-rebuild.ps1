# restart builds for tag

# if ($Env:APPVEYOR_REPO_TAG -eq "true") {
# 	if ($Env:CUSTOM_BUILD_TAG -eq "true") {
# 		echo "Build tag with custom tunings"
# 	} else {
# 		echo "Trying to build tag without custom tunings"
# 		Start-AppveyorBuild `
# 			-ApiKey $env:CUSTOM_API_KEY `
# 			-ProjectSlug 'route4me-python-sdk' `
# 			-Branch $Env:APPVEYOR_REPO_TAG_NAME `
# 			-EnvironmentVariables @{ CUSTOM_BUILD_TAG='true' }

# 		Exit-AppveyorBuild
# 	}
# }
