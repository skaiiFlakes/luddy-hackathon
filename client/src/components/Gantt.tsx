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
import { enableRipple } from '@syncfusion/ej2-base';
import { PdfColor } from '@syncfusion/ej2-pdf-export';

enableRipple(true);

function Gantt({ data }: { data: any }) {
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
  const splitterSettings = {
    position: '41%',
  };

  return (
    <div>
      <p className='mx-auto pb-5 text-xl text-center text-gray-700 font-normal leading-relaxed fs521 lg:w-2/3'>
        Expand each strategy to view subtasks.
      </p>

      <GanttComponent
        ref={(gantt: GanttComponent | null) => {
          ganttInst = gantt;
        }}
        dataSource={data}
        taskFields={taskValues}
        editSettings={editOptions}
        splitterSettings={splitterSettings}
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
        created={() => {
          if (ganttInst) ganttInst.collapseAll();
        }}
      >
        <Inject
          services={[Edit, Toolbar, Selection, PdfExport, ExcelExport]}
        ></Inject>
        <ColumnsDirective>
          {/* <ColumnDirective field='TaskID' headerText='ID'></ColumnDirective> */}
          <ColumnDirective
            field='TaskName'
            headerText='Name'
            minWidth='300'
          ></ColumnDirective>
          <ColumnDirective
            field='StartDate'
            format='MM/dd/yy'
            maxWidth='80'
          ></ColumnDirective>
          <ColumnDirective field='Duration' maxWidth='75'></ColumnDirective>
        </ColumnsDirective>
      </GanttComponent>
    </div>
  );
}

export default Gantt;
