import pandas as pd
import numpy as np


class DfComparator:

    def __init__(self):
        pass

    def compare(self, left_df, right_df):
        '''
        Compares two pandas dataframes.
        :param left_df:
        :param right_df:
        :return: pandas dataframe with found differences
        '''
        # normilise indices
        left_df = left_df.copy().reset_index(drop=True)
        left_df = left_df.reindex(sorted(left_df.columns), axis=1)
        right_df = right_df.copy().reset_index(drop=True)
        right_df = right_df.reindex(sorted(right_df.columns), axis=1)

        # validate dataframes before comparison
        if type(left_df.columns) == pd.core.indexes.base.Index:
            if not (left_df.columns == right_df.columns).all():
                error_msg = 'Dataframes contain incomparable columns left_df/right_df: {}/{}'.format(left_df.columns,
                                                                                                     right_df.columns)
                raise Exception(error_msg)

        else:
            if not left_df.columns == right_df.columns:
                error_msg = 'Dataframes contain incomparable columns left_df/right_df: {}/{}'.format(left_df.columns,
                                                                                                     right_df.columns)
                raise Exception(error_msg)

        # normalise column data types
        if any(left_df.dtypes != right_df.dtypes):
            right_df = right_df.astype(left_df.dtypes)

        # compare dataframes
        if left_df.equals(right_df):
            return pd.DataFrame(np.array([]))

        diff = (left_df != right_df) & ~(left_df.isnull() & right_df.isnull())
        diff_stacked = diff.stack()
        modified = diff_stacked[diff_stacked]
        modified.index.names = ['id', 'column_name']
        diff_location = np.where(diff)
        modified_from = left_df.values[diff_location]
        modified_to = right_df.values[diff_location]
        result = pd.DataFrame({
            'left_df': modified_from,
            'right_df': modified_to},
            index=modified.index)

        # reorder columns
        result = result[['left_df', 'right_df']]
        return result