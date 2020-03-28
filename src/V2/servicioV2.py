import requests
import json
import os

api_key = os.environ["API_KEY"]

headers = {'api_key': api_key}

class ServiceForecasting:
    
    def __init__(self):
        # 
        r = requests.get('https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/18087',headers=headers)
        p = r.json()
        data_request = requests.get(p["datos"])
        self.data = data_request.json()

    def predict(self, n_periods):
        try:
            n_p = int(n_periods)
            n_p = int(n_p/24)

            if (n_p > len(self.data[0]["prediccion"]["dia"])): n_p = len(self.data[0]["prediccion"]["dia"])

        except:
            return "{}",404
        
        periodos = []
        t = []
        h = []

        for n in range (n_p):
            for val in self.data[0]["prediccion"]["dia"][n]["temperatura"]:
                periodos.append(val["periodo"])
                t.append(val["value"])
            for val in self.data[0]["prediccion"]["dia"][n]["humedadRelativa"]:
                h.append(val["value"])
                    
        return self.get_json(n_p,periodos,t,h),200


    def get_json(self,n_p,periods,fc_T, fc_H): 
        total = len(periods)
        s = '{ "origen": '+json.dumps(self.data[0]["origen"])+', "forecast": ['
        for n in range(n_p):
            fecha = self.data[0]["prediccion"]["dia"][n]["fecha"]
            s+= '{ "date": "'+fecha+'", "values": ['
            for i in range(total):
                s+='{"hour" : "'+periods[i]+':00", "temp": '+fc_T[i]+', "hum": '+fc_H[i]+'}'
                if i != total-1: s+=","
            s+=']}'
            if n != n_p-1: s+=","
        s += ']}'
        return json.loads(s)