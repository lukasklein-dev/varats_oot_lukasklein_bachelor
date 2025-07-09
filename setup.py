from setuptools import setup, find_packages

setup(
    name="varats_oot_lukasklein_bachelor",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "varats.projects": [
            "sklearn_experiment_sgd = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectSGD",
            "sklearn_experiment_knn = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectKNN",
            "sklearn_experiment_svc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectSVC",
            "sklearn_experiment_rfc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectRFC",
            "sklearn_experiment_bgm = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectBGM",
            "sklearn_experiment_dtc_test = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectDTCTest",
            "sklearn_experiment_dtc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectDTC",
            "sklearn_experiment_etc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectETC",
            "sklearn_experiment_gpc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectGPC",
            "sklearn_experiment_gbc = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectGBC",
            "sklearn_experiment_mnb = varats_oot_lukasklein_bachelor.projects.sklearn:SklearnProjectMNB",
        ],
        "varats.experiments": [
            "SklearnExperiment = varats_oot_lukasklein_bachelor.experiments.sklearn_experiment:SklearnExperiment",
            "SklearnMeasuring = varats_oot_lukasklein_bachelor.experiments.sklearn_experiment:SklearnMeasuring",
        ],
    },
)