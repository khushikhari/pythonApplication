import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import sqlite3

app = dash.Dash(__name__)

def get_data(start_date, end_date, selected_user, search_term):
    conn = sqlite3.connect('example.db')
    query = '''
    SELECT users.name, users.email, SUM(transactions.amount) as total_spent
    FROM users
    LEFT JOIN transactions ON users.user_id = transactions.user_id
    WHERE users.join_date BETWEEN ? AND ?
    '''
    params = [start_date, end_date]
    if selected_user:
        query += ' AND users.name = ?'
        params.append(selected_user)
    if search_term:
        query += ' AND users.email LIKE ?'
        params.append(f'%{search_term}%')
    query += ' GROUP BY users.name'
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_top_spenders():
    conn = sqlite3.connect('example.db')
    query = '''
    SELECT users.name, SUM(transactions.amount) as total_spent
    FROM users
    JOIN transactions ON users.user_id = transactions.user_id
    GROUP BY users.name
    ORDER BY total_spent DESC
    LIMIT 3
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_avg_transaction_amount():
    conn = sqlite3.connect('example.db')
    query = 'SELECT AVG(amount) as avg_amount FROM transactions'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['avg_amount'][0]

def get_users_with_no_transactions():
    conn = sqlite3.connect('example.db')
    query = '''
    SELECT name, email
    FROM users
    WHERE user_id NOT IN (SELECT DISTINCT user_id FROM transactions)
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

app.layout = html.Div([
    html.H1("User Transaction Report"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2022-01-01',
        end_date='2025-12-31',
        display_format='YYYY-MM-DD'
    ),
    dcc.Dropdown(
        id='user-dropdown',
        options=[
            {'label': 'All Users', 'value': ''},
            {'label': 'Amit Kumar', 'value': 'Amit Kumar'},
            {'label': 'Priya Sharma', 'value': 'Priya Sharma'},
            {'label': 'Raj Patel', 'value': 'Raj Patel'},
            {'label': 'Neha Singh', 'value': 'Neha Singh'},
            {'label': 'Arjun Rao', 'value': 'Arjun Rao'},
            {'label': 'Sita Devi', 'value': 'Sita Devi'},
            {'label': 'Ravi Kumar', 'value': 'Ravi Kumar'},
            {'label': 'Meera Joshi', 'value': 'Meera Joshi'},
            {'label': 'Vikram Singh', 'value': 'Vikram Singh'},
            {'label': 'Anita Desai', 'value': 'Anita Desai'}
        ],
        value='',
        clearable=True
    ),
    dcc.Input(
        id='email-search',
        type='text',
        placeholder='Search by email'
    ),
    dcc.RadioItems(
        id='sort-radio',
        options=[
            {'label': 'Sort by Total Spent', 'value': 'total_spent'},
            {'label': 'Sort by Name', 'value': 'name'}
        ],
        value='total_spent'
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart'),
    html.H2("User Transaction Report Table"),
    html.Div(id='user-report-table'),
    html.Div(id='no-transactions-table')
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('user-report-table', 'children'),
     Output('no-transactions-table', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('user-dropdown', 'value'),
     Input('email-search', 'value'),
     Input('sort-radio', 'value')]
)
def update_content(start_date, end_date, selected_user, search_term, sort_by):
    df = get_data(start_date, end_date, selected_user, search_term)
    
    if df.empty:
        return {}, {}, html.Div("No data available for the selected filters."), html.Div("")

    top_spenders_df = get_top_spenders()
    bar_chart = px.bar(top_spenders_df, x='name', y='total_spent', title="Top 3 Spenders")

    conn = sqlite3.connect('example.db')
    transactions_df = pd.read_sql_query('SELECT transaction_date, amount FROM transactions', conn)
    conn.close()
    line_chart = px.line(transactions_df, x='transaction_date', y='amount', title="Transaction Amounts Over Time")

    avg_amount = get_avg_transaction_amount()
    
    if sort_by:
        df = df.sort_values(by=sort_by, ascending=True)
    
    user_report_table = html.Table(
        [html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
    )

    no_transactions_df = get_users_with_no_transactions()
    no_transactions_table = html.Table(
        [html.Tr([html.Th(col) for col in no_transactions_df.columns])] +
        [html.Tr([html.Td(no_transactions_df.iloc[i][col]) for col in no_transactions_df.columns]) for i in range(len(no_transactions_df))]
    )
    
    return bar_chart, line_chart, user_report_table, no_transactions_table

if __name__ == '__main__':
    app.run_server(debug=True)
