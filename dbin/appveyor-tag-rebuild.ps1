# restart builds for tag

if ($Env:APPVEYOR_REPO_TAG == "true") {
	if ($Env:CUSTOM_BUILD_TAG -eq "true") {
		echo "Trying to build tag without custom tunings"
	} else {
		Start-AppveyorBuild \
			-ApiKey $env:CUSTOM_API_KEY
			-ProjectSlug 'route4me-python-sdk'
			-Branch $Env:APPVEYOR_REPO_TAG_NAME
			-EnvironmentVariables @{ CUSTOM_BUILD_TAG='true' }

		Exit-AppveyorBuild
	}
}
