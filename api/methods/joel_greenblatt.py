import pandas as pd
import fundamentus


def filter_info():
    # Exibindo o dataframe conforme o site Fundamentus
    df = fundamentus.get_resultado()

    # Filtrando conforme aplicado pela formula
    # 3 >= P/L =< 13
    # Margem Líquida >= 15%
    # ROE >= 12%
    # Div. Yield >= 6%
    # Liq. 2 meses >= R$1.000.000
    # Cresc. Rec. últimos 5 anos > 0%
    filtro = df[(df.pl >= 3.0) & (df.pl <= 13.0) & (df.mrgliq >= 0.15) & (
        df.roe >= 0.12) & (df.dy >= 0.06) & (df.liq2m >= 1000000) & (df.c5y > 0.0)]

    return filtro


def rank_info(filtro):
    # Criando o dataframe
    df = pd.DataFrame()

    # Criando um range que vá de 1 até o número de ativos existentes no filtro
    df['POS'] = range(1, len(filtro)+1)

    # EV/EBIT - do menor para o maior
    df['EV/EBIT'] = filtro.sort_values(by=['evebit']
                                       ).index[:len(filtro)].values

    # ROIC & DY - do maior para o menor
    df['ROIC'] = filtro.sort_values(
        by=['roic'], ascending=False).index[:len(filtro)].values
    df['DY'] = filtro.sort_values(
        by=['dy'], ascending=False).index[:len(filtro)].values

    return df


def create_table(df):
    a = df.pivot_table(columns='EV/EBIT', values='POS')
    b = df.pivot_table(columns='ROIC', values='POS')
    c = df.pivot_table(columns='DY', values='POS')
    t = pd.concat([a, b, c])
    rank = t.dropna(axis=1).sum()
    dataframe = pd.DataFrame(rank.sort_values())

    return dataframe


def jg_main():
    filtro = filter_info()
    ranking = rank_info(filtro)
    dataframe = create_table(ranking)
    result = list(dataframe.index)

    return result


# jg_main()
