python_requirements(name="3rdparty", module_mapping={"pantsbuild.pants":("pants",)})

file(name="build-root", source="BUILD_ROOT")

__defaults__({
    python_tests: dict(dependencies=["//:build-root"]),
})
