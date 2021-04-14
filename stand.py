from datetime import datetime
import pandas as pd

dstan={
     'plot_nr': 126,
    'cadastral_address':'G020450019-1013 -h -00',
    'forest_compartment':'13h',
    'year_of_inventory':2010,
    'area':0.92,
    'forest_type':'bsw',
    'forest_cover':0.9,
    'species':'Pine',
    'share':10,
    'age':38,
    'dbh':12,
    'height':13,
    'site_index':'II',
    'yield':160,
    'activity':'TWP',
    'area_of_activity':0.92,
    'volume':34
}

class Stand():
    def __init__(self,stand,year):
        #wczytuje tablice ale tu musi byc jakas logika zeby wczytywacodpowiednia tablice
        self.tablica=pd.read_csv('tab.csv')

        self.current_age=self.calculate_current_age(stand['year_of_inventory'],stand['age'],year)
        self.current_large_timber=float(self.tablica.loc[self.tablica['Age']==self.current_age]['LargeTimber'].values[0].replace(',','.'))
        self.current_small_timber=float(self.tablica.loc[self.tablica['Age']==self.current_age]['SmallTimber'].values[0].replace(',','.'))
        self.current_total_timber=self.current_large_timber+self.current_small_timber
        self.corr_factor=self.get_corr_factor(stand)
        self.large_timber_per_area=self.current_large_timber*self.corr_factor*stand['area']
        self.small_timber_per_area=self.current_small_timber*self.corr_factor*stand['area']
        self.total_timber_per_area=self.large_timber_per_area+self.small_timber_per_area
    def calculate_current_age(self,start_year,start_age,year):
        return year-start_year+start_age
    def get_corr_factor(self,stand):
        yield_at_start=float(self.tablica.loc[self.tablica['Age']==stand['age']]['Total'].values[0].replace(',','.'))
        return stand['yield']/yield_at_start

    def print_summary(self):
        print('----------------------------------\n')
        print('Obecny wiek drzewostanu: '+str(self.current_age)+'\n')
        print('Wielkowymiarowe drewno: '+str(self.current_large_timber)+' m3/ha \n')
        print('Malowymiarowe drewno: '+str(self.current_small_timber)+' m3/ha \n')
        print('Suma: '+str(self.current_total_timber)+' m3/ha \n')
        print('----------------------------------\n')
        print('Faktor korygujacy: '+str(round(self.corr_factor*100,1))+' % \n')
        print('Wielkowymiarowe drewno na powierzchni: '+str(round(self.large_timber_per_area,2))+' m3 \n')
        print('Malowymiarowe drewno na powierzchnie: '+str(round(self.small_timber_per_area,2))+' m3 \n')
        print('Suma drewna na powierzchnie: '+str(round(self.total_timber_per_area,2))+' m3 \n')
        print('----------------------------------\n')
    



drzewostan_dzisiaj=Stand(dstan,datetime.today().year)
drzewostan_dzisiaj.print_summary()
#dstan za 15 lat
#cos tutaj nie halo z tymi obliczeniami
dstan_15=Stand(dstan,datetime.today().year+15)
for x in range(15,60):
    dstan_15=Stand(dstan,datetime.today().year+x)
    print(dstan_15.total_timber_per_area)
