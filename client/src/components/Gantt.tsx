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
  TimelineViewMode,
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
    duration: 'Duration',
    dependency: 'Predecessor',
    child: 'subtasks',
  };

  const timelineSettings = {
    timelineViewMode: 'Month',
    topTier: {
      unit: 'Month',
      format: 'MMM yyyy',
    },
    bottomTier: {
      unit: 'Week',
      format: 'dd',
    },
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

    if (args.item.text === 'Week') {
      ganttRef.current.timelineSettings.timelineViewMode = 'Week';
      ganttRef.current.timelineSettings.topTier!.unit = 'Week';
      ganttRef.current.timelineSettings.topTier!.format = 'MMM dd, yyyy';
      ganttRef.current.timelineSettings.bottomTier!.unit = 'Day';
      ganttRef.current.timelineSettings.bottomTier!.format = 'dd';
    } else if (args.item.text === 'Month') {
      ganttRef.current.timelineSettings.timelineViewMode = 'Month';
      ganttRef.current.timelineSettings.topTier!.unit = 'Month';
      ganttRef.current.timelineSettings.topTier!.format = 'MMM yyyy';
      ganttRef.current.timelineSettings.bottomTier!.unit = 'Week';
      ganttRef.current.timelineSettings.bottomTier!.format = 'dd';
    } else if (args.item.text === 'Year') {
      ganttRef.current.timelineSettings.timelineViewMode = 'Year';
      ganttRef.current.timelineSettings.topTier!.unit = 'Year';
      ganttRef.current.timelineSettings.topTier!.format = 'yyyy';
      ganttRef.current.timelineSettings.bottomTier!.unit = 'Month';
      ganttRef.current.timelineSettings.bottomTier!.format = 'MMM';
    }

    // Handle existing export functionality
    if (args.item.id?.includes('pdfexport')) {
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
    } else if (args.item.id?.includes('excelexport')) {
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
    } else if (args.item.id?.includes('csvexport')) {
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
        // @ts-expect-error Description: This error is expected because the type definition for the timelineSettings prop is missing.
        timelineSettings={timelineSettings}
        onTaskbarClick={handleTaskbarClick}
        rowHeight={50}
        taskbarHeight={15}
        allowSelection={true}
        allowPdfExport={true}
        allowExcelExport={true}
        toolbarClick={toolbarBtnClick}
        toolbar={[
          { text: 'Add', tooltipText: 'Add', type: 'Button', align: 'Left' },
          { text: 'Edit', tooltipText: 'Edit', type: 'Button', align: 'Left' },
          {
            text: 'Update',
            tooltipText: 'Update',
            type: 'Button',
            align: 'Left',
          },
          {
            text: 'Cancel',
            tooltipText: 'Cancel',
            type: 'Button',
            align: 'Left',
          },
          {
            text: 'ExpandAll',
            tooltipText: 'Expand All',
            type: 'Button',
            align: 'Left',
          },
          {
            text: 'CollapseAll',
            tooltipText: 'Collapse All',
            type: 'Button',
            align: 'Left',
          },

          {
            text: 'Week',
            tooltipText: 'Week View',
            type: 'Button',
            align: 'Center',
          },
          {
            text: 'Month',
            tooltipText: 'Month View',
            type: 'Button',
            align: 'Center',
          },
          {
            text: 'Year',
            tooltipText: 'Year View',
            type: 'Button',
            align: 'Center',
          },

          {
            text: 'PdfExport',
            tooltipText: 'PDF Export',
            type: 'Button',
            align: 'Right',
          },
          {
            text: 'ExcelExport',
            tooltipText: 'Excel Export',
            type: 'Button',
            align: 'Right',
          },
          {
            text: 'CsvExport',
            tooltipText: 'CSV Export',
            type: 'Button',
            align: 'Right',
          },
        ]}
      >
        <Inject services={[Edit, Toolbar, Selection, PdfExport, ExcelExport]} />
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
              props.TaskID !== 'A' &&
              props.TaskID !== 'B' &&
              props.TaskID !== 'C' ? (
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
