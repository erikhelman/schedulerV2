<template>
    <b-container id="signup">
        <b-row class="justify-content-center">
            <b-card
                header="Registration Form"
                header-bg-variant="secondary"
                header-text-variant="white">
                <b-form @submit.prevent="onSubmit">
                    <b-row>
                        <b-col>
                            <b-form-group
                                    label="First Name:"
                                    label-for="fname">
                                <b-form-input id="fname"
                                    v-model="fname"
                                    :state="(errors.fname) ? false : null">
                                    maxLength="50">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    Please enter your first name
                                </b-form-invalid-feedback>                            
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                    label="Last Name:"
                                    label-for="lname">
                                <b-form-input id="lname"
                                    v-model="lname"
                                    :state="(errors.lname) ? false : null">
                                    maxLength="50">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    Please enter your last name
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                    label="Phone Number"
                                    label-for="phone">
                                <b-form-input id="phone"
                                    v-model="phone"
                                    :state="(errors.phone) ? false : null">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    Please enter a valid phone number
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </b-col>
                        <b-col>
                            <b-form-group
                                    label="Email Address:"
                                    label-for="email">
                                <b-form-input id="email"
                                    v-model="email"
                                    :state="(errors.email) ? false : null"
                                    maxLength="50">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    Please enter a valid email address
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col>
                            <b-form-group
                                    label="Password:"
                                    label-for="password">
                                <b-form-input id="password"
                                    type="password"
                                    v-model="password"
                                    :state="(errors.password) ? false : null"
                                    maxLength="100"
                                    @change="$v.confirmPassword.$touch()">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    Please enter a password
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </b-col>                        
                        <b-col>
                            <b-form-group
                                    label="Confirm Password:"
                                    label-for="confirmPassword">
                                <b-form-input id="confirmPassword"
                                    type="password"
                                    v-model="confirmPassword"
                                    :state="confirmPasswordState"
                                    @change="$v.confirmPassword.$touch()">
                                </b-form-input>
                                <b-form-invalid-feedback>
                                    The password confirmation must match the password
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </b-col>
                    </b-row>                
                    <hr>
                    <h2>Student Information</h2>
                    <div v-for="(student, index) in students" :key=index>
                        <b-row>
                            <b-col>    
                            <h5>Student {{ index + 1 }}</h5>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-button 
                                    :style="{'marginBottom': '1em'}"                            
                                    variant="secondary"
                                    @click="onDeleteStudent(index)">
                                    Delete
                                </b-button>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="First Name">
                                    <b-form-input id="studentFname"
                                        v-model="students[index].fname"
                                        maxLength="25"
                                        :state="(errors.students && errors.students[index] && errors.students[index].fname) ? false : null">
                                    </b-form-input>
                                    <b-form-invalid-feedback>
                                        Please enter the student's first name
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                        description="Last Name">
                                    <b-form-input id="studentLname"
                                        v-model="students[index].lname"
                                        maxLength="25"
                                        :state="(errors.students && errors.students[index] && errors.students[index].lname) ? false : null">
                                    </b-form-input>
                                    <b-form-invalid-feedback>
                                        Please enter the student's last name
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>                        
                            <b-col>
                                <b-form-group
                                        description="Date of Birth">
                                    <b-form-input
                                        v-model="students[index].dob"
                                        :state="(errors.students && errors.students[index] && errors.students[index].dob) ? false : null"
                                        type="date">
                                    </b-form-input>
                                    <b-form-invalid-feedback>
                                        Please enter the student's date of birth
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                        description="Gender">
                                    <b-form-select
                                        id="genders"
                                        :options="genders"
                                        v-model="students[index].gender"
                                        :state="(errors.students && errors.students[index] && errors.students[index].gender) ? false : null">
                                    </b-form-select>
                                    <b-form-invalid-feedback>
                                        Please select the gender of this student
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                        </b-row>    
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="Emergency Contact">
                                    <b-form-input id="emergName"
                                        v-model="students[index].emergName"
                                        maxLength="50"
                                        :state="(errors.students && errors.students[index] && errors.students[index].emergName) ? false : null">
                                    </b-form-input>
                                    <b-form-invalid-feedback>
                                        Please include an emergency contact
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                        description="Emergency Contact Number">
                                    <b-form-input id="emergContact"
                                        v-model="students[index].emergContact"
                                        maxLength="20"
                                        :state="(errors.students && errors.students[index] && errors.students[index].emergContact) ? false : null">
                                    </b-form-input>
                                    <b-form-invalid-feedback>
                                        Please provide the number where the emergency contact can be reached
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="Previous Swim School Attended (if any)">
                                    <b-form-input id="previousSchool"
                                        v-model="students[index].previousSchool"
                                        maxLength="100">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                        description="Level Achieved (if applicable)">
                                    <b-form-input id="level"
                                        v-model="students[index].level"
                                        type="number"
                                        min="0"
                                        max="99">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="Class Type">
                                    <b-form-select
                                        id="classTypes"
                                        :options="classTypes"
                                        v-model="students[index].classType"
                                        :state="(errors.students && errors.students[index] && errors.students[index].classType) ? false : null">
                                    </b-form-select>
                                    <b-form-invalid-feedback>
                                        Please select the type of class for this student
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                        description="Class Length">
                                    <b-form-select
                                        id="classLength"
                                        :options="classLengths"
                                        v-model="students[index].classLength"
                                        :state="(errors.students && errors.students[index] && errors.students[index].classLength) ? false : null">
                                    </b-form-select>
                                    <b-form-invalid-feedback>
                                        Please select the length of class for this student
                                    </b-form-invalid-feedback>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="Day of the Week">
                                    <b-form-select
                                        id="dayOfTheWeek0"
                                        :options="daysOfTheWeek"
                                        v-model="students[index].prefDay[0]">
                                    </b-form-select>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="Start time">
                                    <b-form-input
                                        v-model="students[index].prefStartTime[0]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="End time">
                                    <b-form-input
                                        v-model="students[index].prefEndTime[0]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>                            
                                <b-form-group
                                        description="Day of the Week">
                                    <b-form-select
                                        id="dayOfTheWeek1"
                                        :options="daysOfTheWeek"
                                        v-model="students[index].prefDay[1]">
                                    </b-form-select>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="Start time">
                                    <b-form-input
                                        v-model="students[index].prefStartTime[1]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="End time">
                                    <b-form-input
                                        v-model="students[index].prefEndTime[1]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                        description="Day of the Week">
                                    <b-form-select
                                        id="dayOfTheWeek2"
                                        :options="daysOfTheWeek"
                                        v-model="students[index].prefDay[2]">
                                    </b-form-select>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="Start time">
                                    <b-form-input
                                        v-model="students[index].prefStartTime[2]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    description="End time">
                                    <b-form-input
                                        v-model="students[index].prefEndTime[2]"
                                        type="time">
                                    </b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                    </div>
                    <b-alert 
                        :show="showAlert"
                        variant="danger">
                        {{ registrationError }}
                    </b-alert>
                    <b-button 
                        variant="secondary"
                        @click="onSubmit"
                        :disabled="registerState">
                        Register
                    </b-button>
                    <b-button
                        :style="{ 'marginLeft': '1em' }"
                        variant="secondary"                        
                        @click="onAddStudent"
                        :disabled="registerState">
                        Add Student
                    </b-button>
                </b-form>
            </b-card>
        </b-row>
    </b-container>
</template>
<script>
import axios from 'axios';
import moment from 'moment';
import { parseNumber } from 'libphonenumber-js';
import { required, sameAs, email, minLength } from 'vuelidate/lib/validators';

export default {
    data () {
        return {
            fname: '',
            lname: '',
            phone: '',
            email: '',
            password: '',
            confirmPassword: '',
            registrationError:'',
            showAlert: false,
            registerState: false,
            students: [{
                fname: '',
                lname: '',
                gender: '',
                dob: '',
                classLength: null,
                classType: '',
                previousSchool: '',
                level: null,
                emergName: '',
                emergContact: '',
                pDay: ['','',''],
                pStartTime: [null, null, null],
                pEndTime: [null, null, null],
                pDOB: null,
                prefDay: ['','',''],
                prefStartTime: ['','',''],
                prefEndTime: ['','','']
            }],
            errors: {},
            genders: [{
                value: 'm',
                text: 'Male'
            },
            {   value: 'f',
                text: 'Female'
            }],
            classTypes: [{
                value: 'p',
                text: 'Private'
            },
            {   value: 's',
                text: 'Semi-Private'
            }],
            classLengths: [{
                value: '45',
                text: '45'
            },
            {   value: '60',
                text: '60'
            }],
            daysOfTheWeek: [{
                value: 'Monday',
                text: 'Monday'
            },
            {   value: 'Tuesday',
                text: 'Tuesday'
            },
            {   value: 'Wednesday',
                text: 'Wednesday'
            },
            {   value: 'Thursday',
                text: 'Thursday'
            },
            {   value: 'Friday',
                text: 'Friday'
            },
            {   value: 'Saturday',
                text: 'Saturday'
            },
            {   value: 'Sunday',
                text: 'Sunday'
            }]
        }
    },
    computed: {
        confirmPasswordState: {
            get() {
                return this.$v.confirmPassword.$invalid ? false : null;
            }
        }
    },
    validations: {
        confirmPassword: {
            sameAsPassword: sameAs('password')
        },
        email: {
            required,
            email            
        },
        fname: {
            minLength: minLength(1),
            required
        },
        lname: {
            minLength: minLength(1),
            required
        },
        password: {
            minLength: minLength(1),
            required
        },
        phone: {
            validPhone: p => {
                return Object.keys(parseNumber(p, "CA")).length !== 0;
            }
        },        
        students: {
            $each: {
                fname: {
                    minLength: minLength(1),
                    required
                },
                lname: {
                    minLength: minLength(1),
                    required
                },
                gender: {
                    required
                },
                dob: {
                    required
                },
                classType: {
                    required
                },
                classLength: {
                    required
                },
                emergName: {
                    minLength: minLength(1),
                    required
                },
                emergContact: {
                    minLength: minLength(1),
                    required
                }
            }
        }
    },
    methods: {
        onAddStudent () {
            let newStudent = {
                fname: null,
                lname: '',
                gender: '',
                dob: '',
                classLength: null,
                classType: '',
                previousSchool: '',
                level: null,
                emergName: '',
                emergContact: '',
                pDay: ['','',''],
                pStartTime: [null, null, null],
                pEndTime: [null, null, null],
                pDOB: null,
                prefDay: ['','',''],
                prefStartTime: ['','',''],
                prefEndTime: ['','','']  
            };
            this.students.push(newStudent);
        },
        onDeleteStudent (index) {
            this.students.splice(index, 1);
        },
        onSubmit () {
            
            this.registerState=true;
            
            if (this.validateForm()) {
            
                let email = this.email.trim();
                let fname = this.fname.trim();
                let lname = this.lname.trim();
                let phone = parseNumber(this.phone, "CA");
                let password = this.password;
                let students = this.students;

                students.forEach(function (student) {
                    student.prefStartTime.forEach(function (stTime, index) {
                        if (stTime) {
                            student.pStartTime[index] = moment.utc(stTime, "HH:mm");
                            }
                        })
                    
                    student.prefEndTime.forEach(function (eTime, index) {
                        if (eTime) {
                            student.pEndTime[index] = moment.utc(eTime, "HH:mm");
                            }
                        })
                    
                    student.pDOB = moment(student.dob, "YYYY-MM-DD")

                    })

                axios.post('/register', {
                    fname,
                    lname,
                    email,
                    phone: (phone.phone != null ? phone.phone : ''),
                    password,
                    students
                })

                .then(response => {
                    if (response.data.isRegistered === "true") {
                        this.$router.push({ name: 'success'});                        
                    } else {
                       
                        this.showAlert=true;
                        this.registerState=false;
                        this.registrationError=response.data.errors;
                    }
                })
                .catch(error => {
                    console.log(error)
                })
            } else {

                this.showAlert=true;
                this.registrationError="Please complete all required fields to complete registration."
                this.registerState=false;
            }
        },
        validateForm() {
            
            this.errors = {};

            if (this.$v.$invalid) {
                
                let currentState = this.$v;
                let err = {};
                err.students={};

                err.fname = (currentState.fname.$invalid) ? true : null;
                err.lname = (currentState.lname.$invalid) ? true : null;
                err.phone = (currentState.phone.$invalid) ? true : null;
                err.email = (currentState.email.$invalid) ? true : null;
                err.password = (currentState.password.$invalid) ? true : null;

                this.students.forEach(function (student, index) {

                    if (currentState.students.$each[index].$invalid) {
                        let st = {};
                        st.fname = (currentState.students.$each[index].fname.$invalid) ? true : null;
                        st.lname = (currentState.students.$each[index].lname.$invalid) ? true : null;
                        st.dob = (currentState.students.$each[index].dob.$invalid) ? true : null;
                        st.classType = (currentState.students.$each[index].classType.$invalid) ? true : null;
                        st.classLength = (currentState.students.$each[index].classLength.$invalid) ? true : null;
                        st.gender = (currentState.students.$each[index].gender.$invalid) ? true : null;
                        st.emergName = (currentState.students.$each[index].emergName.$invalid) ? true : null;
                        st.emergContact = (currentState.students.$each[index].emergContact.$invalid) ? true : null;
                        err.students[index] = st;
                        
                    }
                

                })
                this.errors = err;
                return false;
            } else {
                return true;
            };

                
        }
          
        
    }
}
</script>
<style>
    body {    
   
    height: 100%; 

    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}
</style>