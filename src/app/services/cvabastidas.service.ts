import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CvabastidasService {

  profesional: any[] = [];
  educacion: any[] = [];
  testimonio: any[] = [];
  experiencia: any[] = [];
  blog: any[] = [];

  proFL: any[] = [];
  proPL: any[] = [];
  proFr: any[] = [];
  otherTools: any[] = [];

  constructor(private http: HttpClient) {
    this.CargarProfesional();
    this.CargarEducacion();
    this.CargarTestimonio();
    this.CargarExperiencia();
    this.CargarBlog();

    // Professional
    this.CargarProLanguages();
    this.CargarProPL(); // Programming Languages
    this.CargarProFramework();
    this.CargarOtherTools();
  }

  private CargarProfesional() {
    try {
      this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/Profesional.json')
        .subscribe((resp: any) => {
          this.profesional = resp;
          console.log(resp);
        });
    } catch (ex) {
      console.log(ex);
    }
  }

  private CargarProPL() { // Programming Languages
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/ProLanguages.json')
      .subscribe((resp: any) => {
        this.proPL = resp;
        console.log(resp);
      });
  }

  private CargarProFramework() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/ProFramework.json')
      .subscribe((resp: any) => {
        this.proFr = resp;
        console.log(resp);
      });
  }

  private CargarProLanguages() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/ProFLanguages.json')
      .subscribe((resp: any) => {
        this.proFL = resp;
        console.log(resp);
      });
  }

  private CargarOtherTools() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/OtherTools.json')
      .subscribe((resp: any) => {
        this.otherTools = resp;
        console.log(resp);
      });
  }

  private CargarEducacion() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/Educacion.json')
      .subscribe((resp: any) => {
        this.educacion = resp;
        console.log(resp);
      });
  }

  private CargarTestimonio() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/Testimonio.json')
      .subscribe((resp: any) => {
        this.testimonio = resp;
        console.log(resp);
      });
  }

  private CargarExperiencia() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/Experiencia.json')
      .subscribe((resp: any) => {
        this.experiencia = resp;
        console.log(resp);
      });
  }

  private CargarBlog() {
    this.http.get('https://krtucho-portfolio-default-rtdb.firebaseio.com/Blog.json')
      .subscribe((resp: any) => {
        this.blog = resp;
        console.log(resp);
      });
  }
}
