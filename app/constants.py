class TipoDocumentoIdentidad:
    DNI = 'DNI'  # Documento Nacional de Identidad
    CE = 'CE'   # Carnet de Extranjería
    PAS = 'PAS' # Pasaporte
    RUC = 'RUC' # Registro Único de Contribuyentes
    CPP = 'CPP' # Carnet de Permiso Temporal de Permanencia

    @classmethod
    def choices(cls):
        return [
            (cls.DNI, 'DNI'),
            (cls.CE, 'Carnet de Extranjería'),
            (cls.PAS, 'Pasaporte'),
            (cls.RUC, 'RUC'),
            (cls.CPP, 'Carnet PTP')
        ]

class TipoObra:
    # Industria
    PLANTA_CEMENTO = 'Planta de Cemento y Cal'
    NAVES_INDUSTRIALES = 'Naves Industriales'
    HIDROELECTRICA = 'Hidroeléctrica'
    CENTRAL_TERMO = 'Central Termoeléctrica'
    PLANTA_ELECTRICA = 'Planta Eléctrica'
    PUENTES = 'Puentes'
    PLANTA_PETROLEO = 'Planta Petróleo'
    OBRAS_CIVILES = 'Obras Civiles'
    
    # Minería
    PLANTA_GAS = 'Planta de Gas'
    CONST_ESTRUCTURAS = 'Construcción Estructuras'
    MONTAJE_ESTRUCTURAS = 'Montaje de Estructura Pesada'
    CHANCADORA_FAJAS = 'Chancadora/Fajas (seca)'
    MOLINOS_FLOTACION = 'Molinos/Celda de Flotación'
    TUNELES = 'Túneles'
    DESMONTAJE = 'Desmontaje'
    
    # Servicios
    ELECTRICIDAD_INSTR = 'Electricidad & Instrumentación'
    TUBERIA_AGUA = 'Tubería Agua/Relaves'
    PLANTA_DESALINIZADORA = 'Planta Desalinizadora'
    TRUCKSHOP = 'Truckshop - Almacenes (Auxiliares)'

    @classmethod
    def get_all_tipos(cls):
        return [
            (cls.PLANTA_CEMENTO, 'Industria'),
            (cls.NAVES_INDUSTRIALES, 'Industria'),
            (cls.HIDROELECTRICA, 'Industria'),
            (cls.CENTRAL_TERMO, 'Industria'),
            (cls.PLANTA_ELECTRICA, 'Industria'),
            (cls.PUENTES, 'Industria'),
            (cls.PLANTA_PETROLEO, 'Industria'),
            (cls.OBRAS_CIVILES, 'Industria'),
            (cls.PLANTA_GAS, 'Minería'),
            (cls.CONST_ESTRUCTURAS, 'Minería'),
            (cls.MONTAJE_ESTRUCTURAS, 'Minería'),
            (cls.CHANCADORA_FAJAS, 'Minería'),
            (cls.MOLINOS_FLOTACION, 'Minería'),
            (cls.TUNELES, 'Minería'),
            (cls.DESMONTAJE, 'Minería'),
            (cls.ELECTRICIDAD_INSTR, 'Servicios'),
            (cls.TUBERIA_AGUA, 'Servicios'),
            (cls.PLANTA_DESALINIZADORA, 'Servicios'),
            (cls.TRUCKSHOP, 'Servicios')
        ]