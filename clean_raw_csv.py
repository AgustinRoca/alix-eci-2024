import pandas as pd

from parcels import get_parcels_data

def get_parcel_id(row):
    return int(row['idParcela'].split('-')[0])

def main():

    # Define paths to shapefile and TIFF files
    sanroque_shapefile_path = 'data/parcelas_sanroque.shp'
    santiago_shapefile_path = 'data/parcelas_santiago.shp'
    tiff_paths = {
        'dnbr': 'satimgs/dnbr.tif',
        'sep_ndvi': 'satimgs/sep/ndvi.tif',
        'nov_ndvi': 'satimgs/nov/ndvi.tif'
    }

    # Call the function and get the result
    sanroque_result = get_parcels_data(sanroque_shapefile_path, tiff_paths)
    result_filtered_sanroque = {
        key: {
            'id': value['par_idparc'],
            'tipo': value['Tipo_Parce'].lower(),
            'estado': value['Estado'].lower(),
            'fxf': value['fxf'],
            'valuacion': value['Valuacion'],
            'superficie': value['Superficie'],
            'departamento': value['departamen'].lower() if value['departamen'] else None,
            'pedania': value['pedania'].lower() if value['pedania'] else None,
            'localidad': value['localidad'].lower() if value['localidad'] else None,
            'dnbr': value['dnbr'],
            'sep_ndvi': value['sep_ndvi'],
            'nov_ndvi': value['nov_ndvi']
        } for key, value in sanroque_result.items()
    }

    santiago_result = get_parcels_data(santiago_shapefile_path, tiff_paths)
    result_filtered_santiago = {
        key: {
            'id': value['par_idparc'],
            'tipo': value['Tipo_Parce'].lower(),
            'estado': value['Estado'].lower(),
            'fxf': value['fxf'],
            'valuacion': value['Valuacion'],
            'superficie': value['Superficie'],
            'departamento': value['departamen'].lower() if value['departamen'] else None,
            'pedania': value['pedania'].lower() if value['pedania'] else None,
            'localidad': value['localidad'].lower() if value['localidad'] else None,
            'dnbr': value['dnbr'],
            'sep_ndvi': value['sep_ndvi'],
            'nov_ndvi': value['nov_ndvi']
        } for key, value in santiago_result.items()
    }

    result_filtered = result_filtered_sanroque | result_filtered_santiago
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