set id (buildah from --pull ubuntu:20.04)
buildah run $id -- apt update
buildah run $id -- mkdir /app

# Set TZ, LC_ALL and LANG
buildah config --env TZ=Asia/Kolkata $id
buildah config --env LC_ALL=C.UTF-8 $id
buildah config --env LANG=C.UTF-8 $id

# Install tzdata first to prevent the dreadful prompt appear in the middle of installing the deps
buildah run $id -- bash -c "DEBIAN_FRONTEND=noninteractive apt install -y tzdata"
buildah run $id -- ln -snf /usr/share/zoneinfo/\$TZ /etc/localtime

# Install dependencies
deno eval "import {deps} from 'https://raw.githubusercontent.com/microsoft/playwright/main/packages/playwright-core/src/utils/nativeDeps.ts'; console.log(deps['ubuntu20.04']['chromium'].join('\n'));" > /tmp/deps.txt
buildah copy $id /tmp/deps.txt /tmp
buildah run $id -- xargs -a /tmp/deps.txt apt install -y

# Change working dir to /app
buildah config --workingdir /app $id

# Copy CLI to /app
buildah copy $id ./dist/cli /app/
buildah config --cmd '[]' $id
buildah config --entrypoint '["/app/cli"]' $id

buildah commit $id rep
buildah rm $id
