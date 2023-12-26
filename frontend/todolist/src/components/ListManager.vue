<template>
    <div>
        <h1 v-if="this.listName">{{ this.listName }}</h1>
        <ErrorComponent :error-message="errorMessage" />
        <div class="toolbar">
            <button class="button" @click="handleDeleteList">Delete Current List</button>
            <NewListComponent @list-created="handleNewList" />
            <SearchListComponent @list-search="HandleSearchTask" />
        </div>
        <ToDoTable :tasks="tasks" @new-task-added="handleNewTask" @delete-task="handleDeleteTask"
            @complete-task="handleCompleteTask" @update-task="handleUpdateTask" />
    </div>
</template>

<script>
import ToDoTable from './ToDoTable.vue';
import NewListComponent from './NewListComponent.vue';
import SearchListComponent from './SearchListComponent.vue';
import ErrorComponent from './ErrorComponent.vue';
import axios from 'axios';

const url_base = "http://127.0.0.1:8000/"
function sortObjectsByProperty(arr, property) {
    return arr.sort((a, b) => {
        if (a[property] < b[property]) {
            return -1;
        }
        if (a[property] > b[property]) {
            return 1;
        }
        return 0;
    });
}

export default {
    data() {
        return {
            errorMessage: '', // Error message state
            listId: null,
            listName: null,
            tasks: []
        };
    },
    components: {
        NewListComponent,
        ToDoTable,
        SearchListComponent,
        ErrorComponent
    },
    methods: {
        async handleNewTask(newTask) {
            try {
                // add new task to db
                await axios.post(
                    url_base + `lists/${this.listId}/tasks`,
                    { list_name: this.listName, description: newTask.description, completed: newTask.completed });
                // get all tasks for the current list
                const response = await axios.post(url_base + 'lists/search', { "list_name": this.listName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.tasks = response.data["tasks"].map(function (obj) { return { id: obj.task_id, description: obj.description, completed: obj.completed } })

                this.tasks = sortObjectsByProperty(this.tasks, "id")
                this.errorMessage = ''
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        },
        async handleDeleteTask(taskID) {
            try {
                await axios.delete(url_base + `/lists/${this.listId}/tasks/${taskID}`)
                const response = await axios.post(url_base + 'lists/search', { "list_name": this.listName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.tasks = response.data["tasks"].map(function (obj) { return { id: obj.task_id, description: obj.description, completed: obj.completed } })
                this.tasks = sortObjectsByProperty(this.tasks, "id")
                this.errorMessage = ''
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        },
        async handleCompleteTask(taskID) {
            try {
                await axios.put(url_base + `/lists/${this.listId}/tasks/${taskID}/complete`)
                const response = await axios.post(url_base + 'lists/search', { "list_name": this.listName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.tasks = response.data["tasks"].map(function (obj) { return { id: obj.task_id, description: obj.description, completed: obj.completed } })
                console.log(this.tasks)
                this.tasks = sortObjectsByProperty(this.tasks, "id")
                console.log(this.tasks)
                this.errorMessage = ''
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        }, async handleUpdateTask(taskID, newDescription) {
            try {
                await axios.put(url_base + `/lists/${this.listId}/tasks/${taskID}`, { "description": newDescription })
                const response = await axios.post(url_base + 'lists/search', { "list_name": this.listName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.tasks = response.data["tasks"].map(function (obj) { return { id: obj.task_id, description: obj.description, completed: obj.completed } })
                this.tasks = sortObjectsByProperty(this.tasks, "id")
                this.errorMessage = ''
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        },
        async handleNewList(newListName) {
            try {
                var response = await axios.post(url_base + 'lists', { "list_name": newListName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.listName = newListName
                response = await axios.post(url_base + 'lists/search', { "list_name": this.listName },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.listId = response.data["list_id"]
                this.errorMessage = ''
                this.tasks = []
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        },
        async HandleSearchTask(list_name) {
            try {
                const response = await axios.post(url_base + 'lists/search', { "list_name": list_name },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                this.listId = response.data["list_id"]
                this.listName = list_name
                this.tasks = response.data["tasks"].map(function (obj) { return { id: obj.task_id, description: obj.description, completed: obj.completed } })
                this.tasks = sortObjectsByProperty(this.tasks, "id")
                this.errorMessage = ''
            } catch (error) {
                this.errorMessage = error.response["data"];
            }
        },
        async handleDeleteList() {
            try {
                if (this.listId) {
                    await axios.delete(url_base + `/lists/${this.listId}`)
                    this.listId = null
                    this.listName = null
                    this.tasks = []
                }
            } catch (error) {
                this.errorMessage = error.response.data
                // console.log(error)
            }
        }
    },
};
</script>
<style>
.button {
    background-color: #4CAF50;
    /* Green background */
    border: none;
    color: white;
    /* White text */
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
    /* Rounded corners */
    transition: background-color 0.3s, box-shadow 0.3s;
    /* Smooth transition for hover effect */
}

.button:hover {
    background-color: #45a049;
    /* Darker shade of green */
    box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    /* Add a shadow on hover */
}

.input-field {
    padding: 15px 32px;
    /* Same padding as the button for consistent size */
    font-size: 16px;
    /* Same font size as the button */
    border: 2px solid #4CAF50;
    /* Border color similar to the button's background */
    border-radius: 12px;
    /* Rounded corners like the button */
    margin: 4px 2px;
    /* Same margin as the button */
    outline: none;
    /* Removes the default focus outline */
    transition: border-color 0.3s;
    /* Smooth transition for focus effect */
}

.input-field:focus {
    border-color: #45a049;
    /* Changes border color on focus */
}

.toolbar {
    display: flex;
    /* Use Flexbox */
    align-items: center;
    /* Vertically center items */
    gap: 10px;
    /* Add some space between items */
    justify-content: center;
}

.toolbar .input-field,
.toolbar .button {
    /* flex: 1; */
    /* Each item takes equal space */
}



</style>
