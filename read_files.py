"""
Este archivo tiene las funciones para leer los archivos XLM y descargar los nodos útiles
"""
import xml.etree.ElementTree as Et

# INDICADORES A FILTRAR ---------------------------------------------------------------------------------------------
indicadores_de_muerte = ["Number of deaths", "Number of infant deaths", "Number of under-five deaths",
                    "Mortality rate for 5-14 year-olds (probability of dying per 1000 children aged 5-14 years)",
                    "Adult mortality rate (probability of dying between 15 and 60 years per 1000 population)",
                    "Estimates of number of homicides", "Crude suicide rates (per 100 000 population)",
                    "Mortality rate attributed to unintentional poisoning (per 100 000 population)",
                    "Number of deaths attributed to non-communicable diseases, by type of disease and sex",
                    "Estimated road traffic death rate (per 100 000 population)",
                    "Estimated number of road traffic deaths", "Estimates of rates of homicides per 100 000 population"]

indicadores_de_peso = ["Mean BMI (crude estimate)", "Mean BMI (kg/m&#xb2;) (crude estimate)",
                       "Mean BMI (age-standardized estimate)", "Mean BMI (kg/m&#xb2;) (age-standardized estimate)",
                       "Prevalence of obesity among adults, BMI > 30 (age-standardized estimate) (%)",
                       "Prevalence of obesity among children and adolescents, BMI > +2 standard deviations above the median (crude estimate) (%)",
                       "Prevalence of overweight among adults, BMI > 25 (age-standardized estimate) (%)",
                       "Prevalence of overweight among children and adolescents, BMI > +1 standard deviations above the median (crude estimate) (%)",
                       "Prevalence of underweight among adults, BMI < 18.5 (age-standardized estimate) (%)",
                       "Prevalence of thinness among children and adolescents, BMI < -2 standard deviations below the median (crude estimate) (%)",
                       "Prevalence of overweight among adults, BMI &GreaterEqual; 25 (age-standardized estimate) (%)",
                       "Prevalence of underweight children under 5 years of age   (% weight-for-age <-2 SD) (%)"]

otros_indicadores = ["Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)",
                      "Estimate of daily cigarette smoking prevalence (%)",
                     "Estimate of daily tobacco smoking prevalence (%)",
                     "Estimate of current cigarette smoking prevalence (%)",
                     "Estimate of current tobacco smoking prevalence (%)",
                     "Mean systolic blood pressure (crude estimate)",
                     "Mean fasting blood glucose (mmol/l) (crude estimate)",
                     "Mean Total Cholesterol (crude estimate)"]

mis_indicadores = ["Prevalence of obesity among adults, BMI &GreaterEqual; 30 (age-standardized estimate) (%)",
                   "Number of deaths attributed to non-communicable diseases, by type of disease and sex"]

total_indicadores = indicadores_de_muerte + indicadores_de_peso + otros_indicadores + mis_indicadores
# ------------------------------------------------------------------------------------------------------------------

# Nodos pedidos en el enunciado de la tarea (corresponderán a las columnas de mi archivo)
nodos_necesarios = ["GHO", "COUNTRY", "SEX", "YEAR", "GHECAUSES", "AGEGROUP", "Display", "Numeric", "Low", "High"]


# Función auxiliar
def catch_attribute_error_text(text_to_find, facts):
    """
    Función que obtiene el text del Element que le pido en la rama.
    Me permite obtener la información en específico del Fact (elementos del archivo)

    :param facts: TreeElement del que voy a obtener el parámetro text_to_find
    :param text_to_find: parámetro a encontrar del fact que puede ser "GHO", "COUNTRY", etc.
    :return: si el tipo del elemento no es NoneType entonces retorna el texto del parámetro que mandé a encontrar,
    en otro caso, retorna "None" o -0.1 si el dato no existe.
    """
    if text_to_find in ["Numeric", "High", "Low"]:
        try:
            return float(facts.find(text_to_find).text)
        except AttributeError:
            return -0.1
    else:
        try:
            return facts.find(text_to_find).text
        except AttributeError:
            return "None"


# Función principal
def obtener_data(filename):
    """
    Función que, dado un nombre de archivo XML lo lee, lo transforma en un ElementTree y lo lee, obteniendo los
    nodos requeridos para la tarea
    :param filename: nombre del archivo
    :return: list: lista de diccionarios de los elementos que me interesan dentro del archivo
    """
    # obtengo la información del archivo
    mydoc = Et.parse(filename)

    # Obtengo el documento completo en forma de Element (del tree del XML)
    root = mydoc.getroot()

    # Lista de los datos que están relacionados a los indicadores pedidos (corresponderán a las filas en el archivo)
    datos_que_si_me_interesan = []

    for facts_root in root:
        # Diccionario para cada uno de los datos
        fact_dict = dict()

        # Por cada nodo en nodos necesarios, creo una key y de value, obtengo el texto del Fact correspondiente
        for nodo in nodos_necesarios:
            fact_dict[nodo] = catch_attribute_error_text(nodo, facts_root)

        # Ahora filtro, si el "GHO" está dentro de los indicadores solicitados a filtrar, entonces guardo su diccionario
        if fact_dict["GHO"] in total_indicadores:
            datos_que_si_me_interesan.append(fact_dict)

    # Retornamos una lista de los datos que si nos interesan para guardar en el archivo excel
    return datos_que_si_me_interesan

"""
# Test
filename_test = "data_USA.xml"
data = obtener_data(filename_test)
for diccionario_fila in data:
    print(diccionario_fila)"""

