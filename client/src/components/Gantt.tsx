import React from 'react';
import {
  GanttComponent,
  TaskFieldsModel,
  ColumnsDirective,
  ColumnDirective,
  Edit,
  Inject,
  Toolbar,
  Selection,
  PdfExport,
  ExcelExport,
} from '@syncfusion/ej2-react-gantt';
import { PdfColor } from '@syncfusion/ej2-pdf-export';

function Gantt({ data }) {
  let ganttInst: GanttComponent | null;
  const editOptions: any = {
    allowEditing: true,
    allowAdding: true,
    allowDeleting: true,
    allowTaskbarEditing: false,
    mode: 'Normal',
    allowTaskOverlap: true,
    validateMode: 'External',
  };
  const taskValues: TaskFieldsModel = {
    id: 'TaskID',
    name: 'TaskName',
    startDate: 'StartDate',
    endDate: 'EndDate',
    duration: 'Duration',
    dependency: 'Predeceesor',
    child: 'subtasks',
  };
  const toolbarBtnClick = (args: any) => {
    if (args.item.id.includes('pdfexport')) {
      (ganttInst as GanttComponent).pdfExport({
        fileName: 'projectData.pdf',
        enableFooter: false,
        showPredecessorLines: false,
        theme: 'Fabric',
        ganttStyle: {
          taskbar: {
            taskColor: new PdfColor(240, 128, 128),
            taskBorderColor: new PdfColor(240, 128, 128),
            progressColor: new PdfColor(205, 92, 92),
          },
        },
      });
    } else if (args.item.id.includes('excelexport')) {
      (ganttInst as GanttComponent).excelExport({
        fileName: 'projectData.xlsx',
        theme: {
          header: { fontColor: '#C67878' },
          record: { fontColor: '#C67878' },
        },
        header: {
          headerRows: 1,
          rows: [
            {
              cells: [
                {
                  colSpan: 4,
                  value: 'Project Time Tracking Report',
                  style: { fontSize: 20, hAlign: 'Center' },
                },
              ],
            },
          ],
        },
        // footer: {
        //   footerRows: 1,
        //   rows: [
        //     {
        //       cells: [
        //         {
        //           colSpan: 4,
        //           value: 'Visit Again !!!',
        //           style: { fontSize: 18, hAlign: 'Center' },
        //         },
        //       ],
        //     },
        //   ],
        // },
      });
    } else if (args.item.id.includes('csvexport')) {
      (ganttInst as GanttComponent).csvExport();
    }
  };

  return (
    <div>
      <GanttComponent
        ref={(gantt) => (ganttInst = gantt)}
        dataSource={data}
        taskFields={taskValues}
        editSettings={editOptions}
        toolbar={[
          'Add',
          'Edit',
          'Delete',
          'Update',
          'Cancel',
          'ExpandAll',
          'CollapseAll',
          'PdfExport',
          'ExcelExport',
          'CsvExport',
        ]}
        allowSelection={true}
        allowPdfExport={true}
        allowExcelExport={true}
        toolbarClick={toolbarBtnClick}
      >
        <Inject
          services={[Edit, Toolbar, Selection, PdfExport, ExcelExport]}
        ></Inject>
        <ColumnsDirective>
          {/* <ColumnDirective field='TaskID' headerText='ID'></ColumnDirective> */}
          <ColumnDirective field='TaskName' headerText='Name'></ColumnDirective>
          <ColumnDirective
            field='StartDate'
            format='dd-MMM-yy'
          ></ColumnDirective>
          <ColumnDirective field='Duration'></ColumnDirective>
        </ColumnsDirective>
      </GanttComponent>
    </div>
  );
}

export default Gantt;
