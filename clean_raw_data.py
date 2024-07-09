import pandas as pd

from parcels import get_parcels_data

def get_parcel_id(row):
    return int(row['idParcela'].split('-')[0])

def rename_columns(result):
    result_filtered = {
        key: {
            'id': value['par_idparc'],
            'nomenclatura': value['Nomenclatu'],
            'tipo': value['Tipo_Parce'].lower(),
            'tipo_valuacion': value['Tipo_Valua'].lower(),
            'estado': value['Estado'].lower(),
            'designacion_oficial': value['desig_ofic'],
            'expediente_creacion': value['exp_creaci'],
            'fecha_creacion': value['Fecha_Crea'],
            'fecha_alta': value['fecha_alta'],
            'frente_y_fondo': value['fxf'],
            'vut_vigente': value['vut_vigent'],
            'valuacion_fiscal': value['Valuacion'],
            'vigencia_desde': value['vigencia_d'],
            'porcentaje_copropiedad': value['porcentaje'],
            'superficie_urbana': value['Superficie'],
            'valuacion_urbana': value['Valuacion_'],
            'base_imponible_urbana': value['base_impon'],
            'superficie_rural': value['Superfici0'],
            'valuacion_rural': value['Valuacion0'],
            'base_imponible_rural': value['base_impo0'],
            'superficie_mejoras': value['Superfici1'],
            'valuacion_mejoras': value['Valuacion1'],
            'base_imponible_mejoras': value['base_impo1'],
            'cantidad_cuentas': value['Cantidad_C'],
            'departamento': value['departamen'].lower() if value['departamen'] else None,
            'pedania': value['pedania'].lower() if value['pedania'] else None,
            'localidad': value['localidad'].lower() if value['localidad'] else None,
            'ped_nomenclatura': value['ped_nomenc'],
            'nro_cuenta': value['Nro_Cuenta'],
            'row_number': value['row_number'],
            'sep_ndvi': value['sep_ndvi'],
            'nov_ndvi': value['nov_ndvi'],

            'par_entity': value['par_entity'],
            'geometry': value['geometry'],
            'dnbr': value['dnbr'],
        } for key, value in result.items()
    }
    return result_filtered

def main():

    # Define paths to shapefile and TIFF files
    sanroque_shapefile_path = 'data/parcelas_sanroque.shp'
    santiago_shapefile_path = 'data/parcelas_santiago.shp'
    tiff_paths = {
        'dnbr': 'satimgs/dnbr.tif',
        'sep_ndvi': 'satimgs/sep/ndvi.tif',
        'nov_ndvi': 'satimgs/nov/ndvi.tif'
    }

    santiago_result = get_parcels_data(santiago_shapefile_path, tiff_paths)
    santiago_result_filtered = rename_columns(santiago_result)

     # Call the function and get the result
    sanroque_result = get_parcels_data(sanroque_shapefile_path, tiff_paths)
    sanroque_result_filtered = rename_columns(sanroque_result)


    result_filtered = santiago_result_filtered | sanroque_result_filtered
    map_data = pd.DataFrame(result_filtered.values())

    # Open the claims CSV file using pandas

    claims_data = pd.read_csv('data/Claims-WorkingFile_v2.csv')
    claims_data['id'] = claims_data.apply(get_parcel_id, axis=1)

    # Merge the claims DataFrame with the parcels DataFrame
    merged = pd.merge(claims_data, map_data, left_on='id', right_on='id', how='left')

    # Save the merged DataFrame to a new CSV file
    merged.to_csv('data/clean_raw_data.csv', index=False)


if __name__ == '__main__':
    main()