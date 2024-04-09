from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine
import pandas as pd
import numpy as np
from sqlalchemy import text


def group_column_in_arrays(df: pd.DataFrame, column1: str, column2: str) -> np.ndarray:
    column1_selected = df[column1]
    column2_selected = df[column2]
    array_2d = np.column_stack((column1_selected, column2_selected))
    return array_2d.tolist()


def prepare_series(df: pd.DataFrame, params: list[str]) -> list:
    series = []

    for param in params:
        series.append({
            'name': param.split('_')[-1].lower(),
            'data': group_column_in_arrays(df, 'Simulation_Examples_Functions_Sine1_TIMESTAMP', param)
        })

    return series


def get_all_data(db: Session):
    df = pd.read_sql_table('datos', con=engine, parse_dates={'Simulation_Examples_Functions_Sine1_TIMESTAMP': '%Y-%m-%d %H:%M:%S'})
    df.sort_values(by='Simulation_Examples_Functions_Sine1_TIMESTAMP', inplace=True)
    last_timestamp = df['Simulation_Examples_Functions_Sine1_TIMESTAMP'].iloc[-1]
    df['Simulation_Examples_Functions_Sine1_TIMESTAMP'] = (df['Simulation_Examples_Functions_Sine1_TIMESTAMP'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
    headers = ['Simulation_Examples_Functions_Sine1_VALUE']
    series = prepare_series(df, headers)
    return series, last_timestamp


def get_new_data(db: Session, last_timestamp):
    if last_timestamp is None:
        return get_all_data(db)

    statement = text(
        'SELECT * FROM datos WHERE Simulation_Examples_Functions_Sine1_TIMESTAMP > :last_timestamp'
    ).bindparams(last_timestamp=pd.Timestamp(last_timestamp, unit='ms'))

    df = pd.read_sql_query(
        statement,
        con=engine,
        parse_dates={'Simulation_Examples_Functions_Sine1_TIMESTAMP': '%Y-%m-%d %H:%M:%S'}
    )

    df.sort_values(by='Simulation_Examples_Functions_Sine1_TIMESTAMP', inplace=True)
    df['Simulation_Examples_Functions_Sine1_TIMESTAMP'] = (df[
                                                               'Simulation_Examples_Functions_Sine1_TIMESTAMP'] - pd.Timestamp(
        "1970-01-01")) // pd.Timedelta('1ms')
    headers = ['Simulation_Examples_Functions_Sine1_VALUE']
    series = prepare_series(df, headers)
    return series