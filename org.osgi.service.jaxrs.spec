Name:		org.osgi.service.jaxrs
Version:	1.0.1
Release:	1
Summary:	OSGi JAX-RS Whiteboard API
Group:		Development/Java
License:	ASL 2.0
URL:		https://docs.osgi.org/
Source0:	https://repo1.maven.org/maven2/org/osgi/org.osgi.service.jaxrs/%{version}/org.osgi.service.jaxrs-%{version}-sources.jar
Source1:	https://raw.githubusercontent.com/osgi/osgi/r8-cmpn-final/LICENSE#/org.osgi.service.jaxrs-%{version}-LICENSE

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(javax.ws.rs:javax.ws.rs-api)
BuildRequires:	mvn(org.osgi:org.osgi.util.promise)
BuildRequires:	mvn(org.osgi:osgi.core)
BuildRequires:	mvn(org.osgi:osgi.annotation)
BuildRequires:	mvn(org.osgi:org.osgi.service.component)
BuildRequires:	mvn(org.osgi:org.osgi.namespace.implementation)
BuildRequires:	mvn(org.osgi:org.osgi.namespace.service)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
OSGi JAX-RS Whiteboard 1.0.1. PromiseRxInvoker extends
javax.ws.rs.client.RxInvoker and returns an OSGi Promise.
SseEventSourceFactory creates a javax.ws.rs.sse.SseEventSource.
RuntimeDTO extends org.osgi.dto.DTO and references a framework
ServiceReferenceDTO. The whiteboard requirement inlines
osgi.implementation named osgi.jaxrs at version 1.0. JSONRequired
records the application/json media type. The whiteboard packages are
version 1.0.1. The other packages are version 1.0.0. Versioning
annotations are compile-time only. This build targets Java 8.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
rm -rf META-INF
cp -p %{SOURCE1} LICENSE
mkdir -p src/main/java
mv org src/main/java/
python - <<'PY'
from pathlib import Path
root = Path("src/main/java")
javas = sorted(path.relative_to(root).as_posix() for path in root.rglob("*.java"))
expected = [
    "org/osgi/service/jaxrs/client/PromiseRxInvoker.java",
    "org/osgi/service/jaxrs/client/SseEventSourceFactory.java",
    "org/osgi/service/jaxrs/client/package-info.java",
    "org/osgi/service/jaxrs/runtime/JaxrsEndpoint.java",
    "org/osgi/service/jaxrs/runtime/JaxrsServiceRuntime.java",
    "org/osgi/service/jaxrs/runtime/JaxrsServiceRuntimeConstants.java",
    "org/osgi/service/jaxrs/runtime/dto/ApplicationDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/BaseApplicationDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/BaseDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/BaseExtensionDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/DTOConstants.java",
    "org/osgi/service/jaxrs/runtime/dto/ExtensionDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/FailedApplicationDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/FailedExtensionDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/FailedResourceDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/ResourceDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/ResourceMethodInfoDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/RuntimeDTO.java",
    "org/osgi/service/jaxrs/runtime/dto/package-info.java",
    "org/osgi/service/jaxrs/runtime/package-info.java",
    "org/osgi/service/jaxrs/whiteboard/JaxrsWhiteboardConstants.java",
    "org/osgi/service/jaxrs/whiteboard/annotations/RequireJaxrsWhiteboard.java",
    "org/osgi/service/jaxrs/whiteboard/annotations/package-info.java",
    "org/osgi/service/jaxrs/whiteboard/package-info.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JSONRequired.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsApplicationBase.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsApplicationSelect.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsExtension.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsExtensionSelect.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsMediaType.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsName.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsResource.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsWhiteboardTarget.java",
    "org/osgi/service/jaxrs/whiteboard/propertytypes/package-info.java",
]
if javas != expected:
    raise SystemExit("java files changed")
if list(Path(".").rglob("module-info.java")) or list(Path(".").rglob("*.class")):
    raise SystemExit("unexpected input")
license_text = Path("LICENSE").read_text(encoding="utf-8")
if "Apache License" not in license_text or "Version 2.0" not in license_text:
    raise SystemExit("LICENSE is not Apache 2.0")
header = (root / "org/osgi/service/jaxrs/client/PromiseRxInvoker.java").read_text(encoding="utf-8")
if "SPDX-License-Identifier: Apache-2.0" not in header or "Licensed under the Apache License, Version 2.0" not in header:
    raise SystemExit("source license header changed")

Path("pom.xml").write_text('''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>org.osgi.service.jaxrs</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>OSGi JAX-RS Whiteboard</name>
  <description>OSGi JAX-RS Whiteboard %{version}, packaged without a parent POM.</description>
  <url>https://docs.osgi.org/</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>javax.ws.rs</groupId>
      <artifactId>javax.ws.rs-api</artifactId>
      <version>2.1.1</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.util.promise</artifactId>
      <version>1.3.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>6.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.annotation</artifactId>
      <version>8.1.0</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.service.component</artifactId>
      <version>1.5.1</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.namespace.implementation</artifactId>
      <version>1.0.0</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.namespace.service</artifactId>
      <version>1.0.0</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <archive>
            <manifestEntries>
              <Automatic-Module-Name>org.osgi.service.jaxrs</Automatic-Module-Name>
              <Specification-Version>1.0</Specification-Version>
              <Implementation-Version>%{version}</Implementation-Version>
            </manifestEntries>
          </archive>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
''', encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
for needle in (
    "<artifactId>org.osgi.service.jaxrs</artifactId>",
    "<artifactId>javax.ws.rs-api</artifactId>",
    "<artifactId>org.osgi.util.promise</artifactId>",
    "<artifactId>osgi.core</artifactId>",
    "<artifactId>osgi.annotation</artifactId>",
    "<artifactId>org.osgi.service.component</artifactId>",
    "<artifactId>org.osgi.namespace.implementation</artifactId>",
    "<artifactId>org.osgi.namespace.service</artifactId>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "</project.build.sourceEncoding>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
if pom.count("<version>1.0.1</version>") != 1 or pom.count("<version>2.1.1</version>") != 1 or pom.count("<version>1.3.0</version>") != 1 or pom.count("<version>6.0.0</version>") != 1 or pom.count("<version>8.1.0</version>") != 1 or pom.count("<version>1.5.1</version>") != 1 or pom.count("<version>1.0.0</version>") != 2 or pom.count("<scope>provided</scope>") != 4:
    raise SystemExit("pom versions changed")
for needle in (
    "junit",
    "SNAPSHOT",
    "<source>",
    "<target>",
    "<parent>",
    "felix",
    "maven-bundle-plugin",
    "<artifactId>org.osgi.framework</artifactId>",
    "<artifactId>org.osgi.dto</artifactId>",
    "<artifactId>org.osgi.resource</artifactId>",
    "<artifactId>org.osgi.util.function</artifactId>",
    "<version>1.0</version>",
    "<version>1.1.0</version>",
    "<version>1.1.1</version>",
    "<version>8.0.1</version>",
    "<version>1.4.0</version>",
    "projectbuild.sourceEncoding",
    "<groupId>org.eclipse.ee4j</groupId>",
):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/org.osgi.service.jaxrs-%{version}.jar --describe-module org.osgi.service.jaxrs > module-describe.txt
grep -q '^org\.osgi\.service\.jaxrs@' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }
python - <<'PY'
import zipfile
from pathlib import Path
jar = Path("target/org.osgi.service.jaxrs-%{version}.jar")
with zipfile.ZipFile(jar) as zf:
    classes = {name for name in zf.namelist() if name.endswith(".class")}
    required = {
        "org/osgi/service/jaxrs/client/PromiseRxInvoker.class",
        "org/osgi/service/jaxrs/client/SseEventSourceFactory.class",
        "org/osgi/service/jaxrs/client/package-info.class",
        "org/osgi/service/jaxrs/runtime/JaxrsEndpoint.class",
        "org/osgi/service/jaxrs/runtime/JaxrsServiceRuntime.class",
        "org/osgi/service/jaxrs/runtime/JaxrsServiceRuntimeConstants.class",
        "org/osgi/service/jaxrs/runtime/dto/ApplicationDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/BaseApplicationDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/BaseDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/BaseExtensionDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/DTOConstants.class",
        "org/osgi/service/jaxrs/runtime/dto/ExtensionDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/FailedApplicationDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/FailedExtensionDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/FailedResourceDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/ResourceDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/ResourceMethodInfoDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/RuntimeDTO.class",
        "org/osgi/service/jaxrs/runtime/dto/package-info.class",
        "org/osgi/service/jaxrs/runtime/package-info.class",
        "org/osgi/service/jaxrs/whiteboard/JaxrsWhiteboardConstants.class",
        "org/osgi/service/jaxrs/whiteboard/annotations/RequireJaxrsWhiteboard.class",
        "org/osgi/service/jaxrs/whiteboard/annotations/package-info.class",
        "org/osgi/service/jaxrs/whiteboard/package-info.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JSONRequired.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsApplicationBase.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsApplicationSelect.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsExtension.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsExtensionSelect.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsMediaType.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsName.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsResource.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/JaxrsWhiteboardTarget.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/package-info.class",
    }
    if classes != required:
        raise SystemExit("class set " + " ".join(sorted(classes ^ required)))
    invoker = zf.read("org/osgi/service/jaxrs/client/PromiseRxInvoker.class")
    if b"javax/ws/rs/client/RxInvoker" not in invoker or b"org/osgi/util/promise/Promise" not in invoker:
        raise SystemExit("promise invoker lost a type")
    factory = zf.read("org/osgi/service/jaxrs/client/SseEventSourceFactory.class")
    if b"javax/ws/rs/sse/SseEventSource" not in factory:
        raise SystemExit("SSE factory lost SseEventSource")
    runtime = zf.read("org/osgi/service/jaxrs/runtime/dto/RuntimeDTO.class")
    if b"org/osgi/dto/DTO" not in runtime or b"org/osgi/framework/dto/ServiceReferenceDTO" not in runtime:
        raise SystemExit("runtime DTO lost a type")
    requirement = zf.read("org/osgi/service/jaxrs/whiteboard/annotations/RequireJaxrsWhiteboard.class")
    if b"org/osgi/annotation/bundle/Requirement" not in requirement or b"osgi.implementation" not in requirement or b"osgi.jaxrs" not in requirement:
        raise SystemExit("whiteboard requirement lost its name")
    if b"org/osgi/namespace/implementation/ImplementationNamespace" in requirement or b"1.0.1" in requirement or b"1.0.0" in requirement:
        raise SystemExit("whiteboard requirement kept a type or the wrong version")
    json_required = zf.read("org/osgi/service/jaxrs/whiteboard/propertytypes/JSONRequired.class")
    if b"javax/ws/rs/core/MediaType" not in json_required or b"application/json" not in json_required or b"org/osgi/service/component/annotations/ComponentPropertyType" not in json_required:
        raise SystemExit("JSONRequired lost its media type")
    for name in (
        "org/osgi/service/jaxrs/whiteboard/package-info.class",
        "org/osgi/service/jaxrs/whiteboard/annotations/package-info.class",
    ):
        data = zf.read(name)
        if b"org/osgi/annotation/versioning/Version" not in data or b"1.0.1" not in data:
            raise SystemExit("package version was not recorded")
    for name in (
        "org/osgi/service/jaxrs/client/package-info.class",
        "org/osgi/service/jaxrs/runtime/package-info.class",
        "org/osgi/service/jaxrs/runtime/dto/package-info.class",
        "org/osgi/service/jaxrs/whiteboard/propertytypes/package-info.class",
    ):
        data = zf.read(name)
        if b"org/osgi/annotation/versioning/Version" not in data or b"1.0.0" not in data or b"1.0.1" in data:
            raise SystemExit("package version was not recorded")
    if any(b"org/osgi/namespace/implementation/ImplementationNamespace" in zf.read(name) or b"org/osgi/namespace/service/ServiceNamespace" in zf.read(name) for name in classes):
        raise SystemExit("namespace class was not inlined")
PY

%files -f .mfiles
%doc LICENSE
