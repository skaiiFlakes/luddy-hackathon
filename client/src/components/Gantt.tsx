import React, { useEffect, useRef } from 'react';
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
import { LuExternalLink } from 'react-icons/lu';

enableRipple(true);

function Gantt({ data }: { data: any }) {
  const ganttRef = useRef<GanttComponent | null>(null);

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

  useEffect(() => {
    const timer = setTimeout(() => {
      if (ganttRef.current) {
        ganttRef.current.collapseAll();
      }
    }, 100);

    return () => clearTimeout(timer);
  }, []);

  const handleTaskbarClick = (args: any) => {
    console.log('Taskbar clicked:', args.data);
  };

  const handleButtonClick = (id: any) => {
    console.log(id, 'clicked');
    const element = document.getElementById(`task-${id}`);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  };

  const toolbarBtnClick = (args: any) => {
    if (!ganttRef.current) return;

    if (args.item.id.includes('pdfexport')) {
      ganttRef.current.pdfExport({
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
      ganttRef.current.excelExport({
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
      });
    } else if (args.item.id.includes('csvexport')) {
      ganttRef.current.csvExport();
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
        ref={ganttRef}
        dataSource={data}
        taskFields={taskValues}
        editSettings={editOptions}
        splitterSettings={splitterSettings}
        onTaskbarClick={handleTaskbarClick}
        rowHeight={50}
        taskbarHeight={15}
        toolbar={[
          'Add',
          'Edit',
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
          <ColumnDirective
            field='TaskID'
            headerText=' '
            width='30'
            template={(props: any) =>
              props.TaskID % 4 === 1 ? (
                <button
                  onClick={() => handleButtonClick(props.TaskID)}
                  className='text-gray-500 group-hover:text-gray-700 transition-colors duration-300'
                >
                  <LuExternalLink style={{ fontSize: '16px' }} />
                </button>
              ) : null
            }
          ></ColumnDirective>
        </ColumnsDirective>
      </GanttComponent>
    </div>
  );
}

export default Gantt;
