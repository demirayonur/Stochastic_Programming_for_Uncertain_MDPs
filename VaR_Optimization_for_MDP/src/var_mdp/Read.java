package var_mdp;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Iterator;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

public class Read {
	
	 String excelFilePath;
	 FileInputStream inputStream;
	 Workbook workbook;
	 
	 public Read(String path){
		 excelFilePath = path; 
		 try {
			inputStream = new FileInputStream(new File(excelFilePath));
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		 try {
		     workbook = new XSSFWorkbook(inputStream);
		} catch (IOException e) {
			e.printStackTrace();
		}
	 }

	 public void read_transition(double[][] distance){
			XSSFSheet sheet = (XSSFSheet) workbook.getSheetAt(0); // which sheet in excel
			Iterator<Row> iterator = sheet.iterator(); // create row iterator
			for (int i = 0; iterator.hasNext(); i++) {
				Row nextRow = iterator.next(); 
				Iterator<Cell> cellIterator = nextRow.cellIterator(); // create cell
				if(i>=1){
					for (int j = 0; cellIterator.hasNext(); j++) { 
						Cell cell = cellIterator.next();
						if(j>=1){
							distance[i-1][j-1]= cell.getNumericCellValue();
						}
					}
				}
			}
		}
}
