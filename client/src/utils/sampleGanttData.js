Object.defineProperty(exports, '__esModule', { value: true });
exports.sampleGanttData = [
  {
    TaskID: 1,
    TaskName: 'Project Initiation',
    subtasks: [
      {
        TaskID: '1A',
        TaskName: 'Identify Site location',

        StartDate: new Date('04/06/2020'),
        Duration: 4,
      },
      {
        TaskID: '1B',
        TaskName: 'Perform Soil test',

        StartDate: new Date('04/10/2020'),
        Duration: 4,

        Predeceesor: '2FS',
      },
      {
        TaskID: '1C',
        TaskName: 'Soil test approval',

        StartDate: new Date('04/12/2020'),
        Duration: 4,
      },
    ],
  },
  {
    TaskID: 5,
    TaskName: 'Project Estimation',
    subtasks: [
      {
        TaskID: 'A',
        TaskName: 'Develop floor plan for estimation',
        StartDate: new Date('04/03/2020'),
        Duration: 3,
      },
      {
        TaskID: 7,
        TaskName: 'List materials',
        StartDate: new Date('04/04/2020'),
        Duration: 3,
      },
      {
        TaskID: 8,
        TaskName: 'Estimation approval',
        StartDate: new Date('04/08/2020'),
        Duration: 3,
      },
    ],
  },
];
