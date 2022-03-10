# Commands for building dev images (these should be in a different script):
# docker buildx build --platform linux/arm/v7 -f Dockerfile.dev -t lukadd16/nbc-boterator:X.Y.Z-armv7 .
# docker buildx build --platform linux/amd64 -f Dockerfile.dev -t lukadd16/nbc-boterator:X.Y.Z-amd64 .


# In addition to ^^, should also run the cmd that exports the armv7 version (but cd into the 'My Programming/Docker/Exported Images' dir):
# docker save -o nbc-boterator-X.Y.Z-armv7.tar lukadd16/nbc-boterator:X.Y.Z-armv7
# NOTE: try getting this to work with gzip or other more compact file archive (I want to minimize how many MB I need to upload to the RPi each time)
# Also, run this cmd

function Initialize-DockerImages {

    <#
        .SYNOPSIS
            This executes the necessary commands to build (and optionally export) docker images for this project.

        .DESCRIPTION
            This executes the necessary commands to build (and optionally export) docker images for this project.

        .PARAMETER Version
            Specify the project version number associated with the docker images to be created.

        .PARAMETER OutputPath
            Optional parameter. Specify the path to the directory in which tarred backups of the docker images should be saved.
            Without specifying this parameter, images will be saved to the current user's home directory.

       .PARAMETER Production
            Optional parameter. Specify whether to build images for a production or development environment.

            NOTE: the default value is false. To set it to true, append the `-Production` switch alongside the other parameters
            
        .PARAMETER CleanBuild
            Optional parameter. Specify whether or not "clean" docker images should be built.
            This forces docker to ignore existing cached files/layers and forces docker to pull the latest version of the base image.

            NOTE: the default value is false. To set it to true, append the `-CleanBuild` switch alongside the other parameters.

        .EXAMPLE
            PS C:\> powershell -command "& { . .\Initialize-DockerImages.ps1; Initialize-DockerImages -Version '1.8.3' -Production}"

            Description
            ---
            Builds docker images for production, using the version number 1.8.3 in the image's tag.

        .EXAMPLE
            PS C:\> powershell -command "& { . .\Initialize-DockerImages.ps1; Initialize-DockerImages -Version '1.8.2-preview'}"

            Description
            ---
            Builds docker images for a development environment, using the version number 1.8.2-preview in the image's tag.

        .NOTES
            Modified Date: 2022-02-22
            ---
            Version 1.0 - Initial Version
    #>

    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]
        $Version,

        [Alias("Path")]
        [string]
        $OutputPath = $HOME,

        [switch]
        $Production = $false,

        [switch]
        $CleanBuild = $false
    )

    # End execution of this function at the first sign of a (terminating) error
    $ErrorActionPreference = "Stop"

    # Create formatted strings for the file archive and tag names
    $ArmArchiveName = "nbc-boterator:{0}-armv7" -f $Version
    $PCArchiveName = "nbc-boterator:{0}-amd64" -f $Version
    $ArmImageTag = "lukadd16/{0}" -f $ArmArchiveName
    $PCImageTag = "lukadd16/{0}" -f $PCArchiveName
    $ArmArchiveFileName = "{0}.tar" -f $ArmArchiveName
    $PCArchiveFileName = "{0}.tar" -f $PCArchiveName

    <#
    Build docker images for various platforms, using the appropriate arguments for production/dev environment, tag (with version #) and clean builds
    #>
    if ($Production -and $CleanBuild) { # Production + build clean image
        docker buildx build --platform linux/arm/v7 --pull --no-cache -t $ArmImageTag .
        docker buildx build --platform linux/amd64 --pull --no-cache -t $PCImageTag .

    } elseif ($Production -and -not($CleanBuild)) { # Production + use cache
        docker buildx build --platform linux/arm/v7 -t $ArmImageTag .
        docker buildx build --platform linux/amd64 -t $PCImageTag .

    } elseif (-not($Production) -and $CleanBuild) { # Development + build clean image
        docker buildx build --platform linux/arm/v7 -f Dockerfile.dev --pull --no-cache -t $ArmImageTag .
        docker buildx build --platform linux/amd64 -f Dockerfile.dev --pull --no-cache -t $PCImageTag .

    } elseif (-not($Production) -and -not($CleanBuild)) { # Development + use cache
        docker buildx build --platform linux/arm/v7 -f Dockerfile.dev -t $ArmImageTag .
        docker buildx build --platform linux/amd64 -f Dockerfile.dev -t $PCImageTag .

    }

    <#
    Backup the newly created docker images to a compressed tar.gzip file in the OutputPath
    #>
    $BeforeLocation = $PSScriptRoot
    Set-Location -Path $OutputPath

    # TODO: try to get gzip to work as I want to minimize the size of the file I need to transfer over to the server
    docker save -o "$($ArmArchiveFileName.Replace(':', "-"))" "$($ArmImageTag)"
    docker save -o "$($PCArchiveFileName.Replace(':', "-"))" "$($PCImageTag)"

    Set-Location -Path $BeforeLocation
}