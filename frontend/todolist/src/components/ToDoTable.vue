<template>
    <div>
        <TaskForm @new-task-created="addNewTask" />
        <div v-for="task in tasks" :key="task.id">
            <ToDoTask :task="task" @complete-task="completeTask" @update-task="updateTask" @delete-task="deleteTask" />
        </div>
    </div>
</template>
  
<script>
import ToDoTask from './ToDoTask.vue';
import TaskForm from './TaskForm.vue';

export default {
    components: {
        ToDoTask,
        TaskForm
    },
    props: ['tasks'],
    watch: {
        tasks(newVal) {
            console.log('Updated tasks in ToDoTable', newVal);
        }
    },
    methods: {
        addNewTask(newTask) {
            // newTask.id = getRandomNumber(1, 1000000);
            this.$emit('new-task-added', newTask);
            // this.tasks.push(newTask);
        },
        completeTask(taskId) {
            this.$emit('complete-task', taskId);
        },
        updateTask(taskId, newDescription) {
            this.$emit("update-task", taskId, newDescription)
            // const modified_task = this.tasks.find(task => task.id === taskId);
            // modified_task.description = newDescription
            // console.log(taskId, newDescription)
        },
        deleteTask(taskId) {
            this.$emit('delete-task', taskId);
        },
    }

};
</script>
  