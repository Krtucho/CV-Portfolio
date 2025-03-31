import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import emailjs from '@emailjs/browser';

@Component({
  selector: 'app-contacto',
  templateUrl: './contacto.component.html',
  styleUrls: ['./contacto.component.css']
})
export class ContactoComponent implements OnInit {
  form: FormGroup = this.fb.group({
    name: '',
    email: '',
    time: '',
    message: ''
  });

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
  }

  async send(){
    emailjs.init("xLHfb7klOGcmWUjUk")
    let response = emailjs.send("service_skq928e","template_mvh422i",{
      name: this.form.value.name,
      email: this.form.value.email,
      time: new Date().toString(),
      message: this.form.value.message,
      });

      alert("Message has been sent");
      this.form.reset();
  }

}
