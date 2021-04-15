from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

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
    def __init__(self,stand):
        #wczytuje tablice ale tu musi byc jakas logika zeby wczytywacodpowiednia tablice
        self.tablica=pd.read_csv('tab.csv')
        try:
            self.current_age=self.calculate_current_age(stand['year_of_inventory'],stand['age'])
        except:
            print("Wiek wykracza poza zakres tabeli, uzywam wieku poczatkowego !!!")
            self.current_age=stand['age']
        self.area=stand['area']
        self.address=stand['cadastral_address']
        self.current_large_timber=float(self.tablica.loc[self.tablica['Age']==self.current_age]['LargeTimber'].values[0].replace(',','.'))
        self.current_small_timber=float(self.tablica.loc[self.tablica['Age']==self.current_age]['SmallTimber'].values[0].replace(',','.'))
        self.current_total_timber=self.current_large_timber+self.current_small_timber
        self.corr_factor=self.get_corr_factor(stand)
        self.large_timber_per_area=self.current_large_timber*self.corr_factor*self.area
        self.small_timber_per_area=self.current_small_timber*self.corr_factor*self.area
        self.total_timber_per_area=self.large_timber_per_area+self.small_timber_per_area
        self.thinning_intensity=0.15
        self.large_timber_share=0.8
        self.small_timbar_share=1-self.large_timber_share
        self.thinning_interval=10
        self.thinning_start=40
        self.harvest_age=100
    def calculate_current_age(self,start_year,start_age):
        return datetime.today().year-start_year+start_age
    def get_corr_factor(self,stand):
        yield_at_start=float(self.tablica.loc[self.tablica['Age']==stand['age']]['Total'].values[0].replace(',','.'))
        return stand['yield']/yield_at_start
    def simulate(self,years):
        simulated_age=self.current_age
        simulated_total_volume=self.total_timber_per_area
        simulation=[]
        
        
        for i in range(years):
            harvest=0
            #regeneration
            if(i+self.current_age==100):
                simulated_age=0
                #print("HARVESTING!")
                harvest=simulated_total_volume
            else:
                if((simulated_age-self.thinning_start)%self.thinning_interval==0 and simulated_age>self.thinning_start and simulated_age!=self.harvest_age):
                    #print("thinning")
                    harvest=simulated_total_volume*self.thinning_intensity
            #przyrost
            try:
                growth_rate=float(self.tablica.loc[self.tablica['Age']==simulated_age]['Increase'].values[0].replace(',','.'))*self.area
            except:
                print("Nie ma wartosci przyrostu w tablicy, uzywam 0")
                growth_rate=0
            
            simulation.append([datetime.today().year+i,simulated_age,growth_rate,simulated_total_volume,harvest])
            #update
            simulated_age=1+simulated_age
            simulated_total_volume=simulated_total_volume-harvest+growth_rate
            #print(i+self.current_age-self.thinning_start)
            

            #print("Wiek:" +str(simulated_age)+" Rok: "+str(datetime.today().year+i))
        df_simulation = pd.DataFrame(simulation, columns=['Year', 'Age', 'Growth rate','Total Volume','Harvested Timber'])    
        title="Prognoza zabiegow dla adresu: "+self.address
        df_simulation.plot(kind='line',x='Year',title=title)
        plt.show()
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
    



drzewostan=Stand(dstan)
#drzewostan.print_summary()
drzewostan.simulate(100)
#dstan za 15 lat
#cos tutaj nie halo z tymi obliczeniami

