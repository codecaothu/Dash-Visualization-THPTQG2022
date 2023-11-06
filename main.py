from dash import Dash, html, dcc
from dash.dependencies import Input,Output
import plotly.express as px
import pandas as pd

app = Dash()
server = app.server

diem_df = pd.read_csv("data/diem_thi_thptqg_2022.csv", delimiter=",", on_bad_lines="skip")
#print(diem_df.head())

# Tính tần suất mỗi giá trị trong cột "toan"
tansuat_toan = diem_df["toan"].value_counts().reset_index()
tansuat_toan.columns = ["Diem", "SoLuong"]

# Tính tần suất mỗi giá trị trong cột "ngu_van"
tansuat_ngu_van = diem_df["ngu_van"].value_counts().reset_index()
tansuat_ngu_van.columns = ["Diem", "SoLuong"]

# Sắp xếp tần suất theo điểm tăng dần
tansuat_toan = tansuat_toan.sort_values(by="Diem")
tansuat_ngu_van = tansuat_ngu_van.sort_values(by="Diem")


# Tao ra 1 list ten cac tinh
# tentinh_list = [{'label': name, 'value': name} for name in diem_df['ten_tinh'].unique()]
tentinh_list=[]
for name in sorted(set(diem_df["ten_tinh"].values)):
    tentinh_list.append({
        "label": name,
        "value": name
    })
  

#Dựng layout:
app.layout=html.Div(
    [
        html.H1("Biểu đồ điểm thi THPTQG 2022", style={"textAlign":"Center"}),
        html.Div(
            [
                 html.Div("Chọn tỉnh: ", style={"textAlign":"Center"}),
                    dcc.Dropdown(
                        id="name_province_dropdown",
                        multi=True,
                        style={"display": "block", "margin-left": "auto",
                                "margin-right": "auto", "width": "60%"},
                        options= tentinh_list,
                        value=[tentinh_list[-1]['value']] #Gia tri chon mac dinh luc dau
                    ),
                    html.Br(),
                    dcc.Graph(id="histogram_toan"),
                    dcc.Graph(id="histogram_ngu_van"),
                    # Thêm dropdown để lựa chọn số lượng bins
                    dcc.Dropdown(
                        id='bin-dropdown',
                        options=[
                            {'label': '100 Bins', 'value': 100},
                            {'label': '200 Bins', 'value': 200},
                            {'label': '300 Bins', 'value': 300}
                        ],
                        value=100  # Giá trị mặc định
                    )
            ]
        )
           
    ]
)

#Phần callback
@app.callback(
    Output('histogram_toan', 'figure'),
    Input('name_province_dropdown','value'), Input('bin-dropdown', 'value')
)
def update_toan(name_province_dropdown, num_bins):
    # Lọc dữ liệu theo các tỉnh được chọn
    filtered_df = diem_df[diem_df['ten_tinh'].isin(name_province_dropdown)]
    
    # Tính tần suất toán theo tỉnh
    tansuat_toan_theo_tinh = filtered_df["toan"].value_counts().reset_index()
    tansuat_toan_theo_tinh.columns = ["Diem", "SoLuong"]
    tansuat_toan_theo_tinh = tansuat_toan_theo_tinh.sort_values(by="Diem")
    
    fig_toan = px.histogram(tansuat_toan_theo_tinh, x="Diem", y="SoLuong", nbins=num_bins, title="Phổ điểm môn Toán")
    return fig_toan

#Phần callback
@app.callback(
    Output('histogram_ngu_van', 'figure'),
    Input('name_province_dropdown','value'), Input('bin-dropdown', 'value')
)

def update_ngu_van(name_province_dropdown, num_bins):
    # Lọc dữ liệu theo các tỉnh được chọn
    filtered_df = diem_df[diem_df['ten_tinh'].isin(name_province_dropdown)]

    #Tính tần suất văn theo tỉnh
    tansuat_ngu_van_theo_tinh = filtered_df["ngu_van"].value_counts().reset_index()
    tansuat_ngu_van_theo_tinh.columns = ["Diem", "SoLuong"]
    tansuat_ngu_van_theo_tinh = tansuat_ngu_van_theo_tinh.sort_values(by="Diem")

    fig_ngu_van = px.histogram(tansuat_ngu_van_theo_tinh, x="Diem", y="SoLuong", nbins=num_bins, title="Phổ điểm môn Văn")
    return  fig_ngu_van


app.run_server(debug=True, port='8080')