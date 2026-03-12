from pathlib import Path
from typing import Any

import pandas as pd

import yaml


def get_problem_data(problem_dir: Path) -> pd.DataFrame:
    """Get data for a single problem.

    Parameters
    ----------
    problem_dir : Path
        Path of the problem directory.

    Returns
    -------
    problem_data : pd.DataFrame
        Data for the problem.
    """
    # Problem YAML file
    with open(problem_dir / 'problem.yml') as problem_file:
        problem = yaml.safe_load(problem_file.read())
    # Usages files
    usages = []
    usages_dir = problem_dir / 'correct-usages'
    for usages_path in usages_dir.iterdir():
        with open(usages_path) as usages_file:
            usages.append(usages_file.read())
    usages = '\n'.join(usages)
    # Information to record
    return pd.DataFrame(data={
        'tag': problem['fix']['tag'],
        'fixed': 'reverted' not in problem['fix'],
        'usages': usages,
    }, index=[f'{problem['project']['name']}_{int(problem_dir.name)}'])


def get_project_data(project_dir: Path) -> pd.DataFrame:
    """Get data for a whole project.

    Parameters
    ----------
    project_dir : Path
        Path of the project directory.

    Returns
    -------
    project_data : pd.DataFrame
        Data for the project.
    """    
    # All API-related problems of project
    api_related_dir = project_dir / 'problems' / 'api-related'
    if not api_related_dir.exists():
        return pd.DataFrame()
    # Individual API-related problems of project
    project_data = []
    for problem_dir in api_related_dir.iterdir():
        problem_data = get_problem_data(problem_dir)
        project_data.append(problem_data)
    return pd.concat(project_data)


def main() -> None:
    """Extract and save data from all projects as a CSV.
    """
    # All projects across all languages
    data = []
    for language_dir in [Path('java-data'), Path('py-data')]:
        for project_dir in language_dir.iterdir():
            project_data = get_project_data(project_dir)
            data.append(project_data)
    data = pd.concat(data)
    # Save data
    data.to_csv('data.csv', index_label='ID')
    data_new = pd.read_csv('data.csv', index_col='ID')
    print(data_new)


if __name__ == '__main__':
    main()
