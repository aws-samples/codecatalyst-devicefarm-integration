// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
const task_guid = Math.random().toString(36).substring(7);

const TEST_URL = process.env.TEST_URL

describe('Todo App Test', () => {

  it('Should create a new task', async () => {
    await browser.url(TEST_URL);
    await browser.maximizeWindow();

    await expect(browser).toHaveTitle('Todo App')

    const createTodoButton = await browser.$('#create-new-button');
    await createTodoButton.click();

    await browser.pause(2000)

    const itemNameBox = await browser.$('//label[text()="Name"]/following::input[1]');
    await itemNameBox.setValue(`MyTask ${task_guid}`);

    const itemDescriptionBox = await browser.$('//label[text()="Description"]/following::textarea[1]');
    await itemDescriptionBox.setValue('My description - this is a really important task that you must complete')

    const submitTodoButton = await browser.$('#submit-button');
    await submitTodoButton.click();

    await browser.pause(2000); // Replace with a better wait strategy
  });

  it('Should complete a task', async () => {
    await browser.url(TEST_URL);

    const taskCreateResult = await browser.$(`//a[text()='MyTask ${task_guid}']/ancestor::div[4]//button`);

    expect(taskCreateResult).toHaveTextContaining('Mark as complete');

    await taskCreateResult.click();

    await browser.pause(2000); // Replace with a better wait strategy
    });

    it('Should complete a task with in 10s', async () => {
    const completeResult = await browser.waitUntil(
      async () => {
        const element = await browser.$(`//a[text()='MyTask ${task_guid}']/ancestor::div[4]//span[text()='Completed']`);
        return element;
      },
      {
        timeout: 10000,
        timeoutMsg: 'Task was not marked as completed within 10 seconds.',
    }
    );

  });
});
