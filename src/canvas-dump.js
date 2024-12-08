// This is to be copy-pasted into the JS console while on the Canvas grades page for each course.
// It will copy a CSV of the assignments/due dates/completion dates for that course to the clipboard.

copy(
  $$('.student_assignment.editable')
    .map((assignment) => ({
      title: assignment.querySelector('.title a').textContent.trim(),
      dueDate: assignment.querySelector('.due').textContent.trim(),
      submitDate: assignment.querySelector('.submitted').textContent.trim(),
    }))
    .map(
      (assignment) =>
        `"${assignment.title.replaceAll('"', '""')}","${assignment.dueDate}","${assignment.submitDate}"`,
    )
    .join('\n'),
)
