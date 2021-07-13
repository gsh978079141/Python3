import pandas as pd

from com.gsh.freqx.utils.mongodb import MongodbUtils


def sensor_join_name():
    """
    正式环境
    STADB库-Data_statistics表-sensor字段
    关联查询
    SiphtumFlatfrom库Sensor表SensorPlace
    获取中文解释
    :return:
    """
    # 获取数据库client
    db_client = MongodbUtils.get_client("192.168.0.110", "27017", "root", "16883883Ftpisbst01")

    # STADB.Data_statistics
    db_client_STADB = db_client['STADB']
    Data_statistics_val = db_client_STADB['Data_statistics'].find({})
    df_Data_statistics = pd.DataFrame.from_records(Data_statistics_val, index=None)
    df_Data_statistics[['sensor']] = df_Data_statistics[['sensor']].astype('str')

    # SiphtumFlatfrom.Sensor
    db_client_SiphtumFlatfrom = db_client['SiphtumFlatfrom']
    Sensor_val = db_client_SiphtumFlatfrom['Sensor'].find({}, {"_id": 1, "SensorPlace": 1})
    df_Sensor = pd.DataFrame.from_records(Sensor_val, index=None)
    df_Sensor[['_id']] = df_Sensor[['_id']].astype('str')

    # SiphtumFlatfrom.Machine
    db_client_SiphtumFlatfrom = db_client['SiphtumFlatfrom']
    Machine_val = db_client_SiphtumFlatfrom['Machine'].find({}, {"_id": 1, "MachineName": 1})
    df_Machine = pd.DataFrame.from_records(Machine_val, index=None)
    df_Machine[['_id']] = df_Machine[['_id']].astype('str')

    # result
    df_merge = pd.merge(df_Data_statistics, df_Sensor, left_on="sensor", right_on="_id", how="left")
    df_merge_machine = pd.merge(df_merge, df_Machine, left_on="DeviceNum", right_on="_id", how="left")
    df_result = df_merge_machine.drop(columns=['_id_y', '_id']).rename(index=str, columns={"_id_x": "id"})
    return df_result


if __name__ == '__main__':
    df = sensor_join_name()
    df.to_csv("./data/sensor_join_name.csv", encoding="utf_8_sig")
