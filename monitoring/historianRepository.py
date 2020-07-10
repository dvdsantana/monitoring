from store import Store

class HistorianRepository(object):
    def get_active_power(self, date_from, date_to):
        db = Store()
        conn = db.create_connection('monitoring-report.db')

        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, power FROM monitoring WHERE date BETWEEN ? AND ?", [date_from, date_to])
            data = cursor.fetchall()        
        
        return data
    
    def get_energy_consumption(self, date_from, date_to):
        db = Store()
        conn = db.create_connection('monitoring-report.db')

        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, energy FROM monitoring WHERE date BETWEEN ? AND ?", [date_from, date_to])
            data = cursor.fetchall()        
        
        return data
    
    