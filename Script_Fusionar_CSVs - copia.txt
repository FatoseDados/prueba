
/**
 * Fusiona múltiples hojas de cálculo externas (en formato CSV) en una sola hoja "DatosMaestros"
 * Los enlaces de origen se leen desde la hoja 'fuentes' (columna A: nombre, columna B: URL CSV)
 */

function actualizarDatosMaestros() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const hojaFuentes = ss.getSheetByName("fuentes");
  const hojaDestino = ss.getSheetByName("DatosMaestros");

  // Limpiar hoja destino (excepto encabezado)
  hojaDestino.getRange("A2:Z").clearContent();

  const fuentes = hojaFuentes.getRange("A2:B" + hojaFuentes.getLastRow()).getValues();
  let filaDestino = 2;

  for (let i = 0; i < fuentes.length; i++) {
    const nombre = fuentes[i][0];
    const url = fuentes[i][1];

    if (!url) continue;

    try {
      const csv = UrlFetchApp.fetch(url).getContentText();
      const datos = Utilities.parseCsv(csv);

      if (datos.length < 2) continue; // sin datos

      const encabezados = datos[0];
      const cuerpo = datos.slice(1);

      // Agregamos columna cliente y ciudad si no existen
      const nuevaData = cuerpo.map(row => {
        const filaExtendida = row.slice(); // copiar
        filaExtendida.push(nombre); // cliente/ciudad desde nombre en hoja 'fuentes'
        return filaExtendida;
      });

      // Escribir datos en hoja destino
      hojaDestino.getRange(filaDestino, 1, nuevaData.length, nuevaData[0].length).setValues(nuevaData);
      filaDestino += nuevaData.length;

    } catch (error) {
      Logger.log("Error al procesar fuente: " + nombre + " → " + error);
    }
  }
}
