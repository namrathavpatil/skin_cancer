from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from employee.forms import EmployeeForm

from django.views.generic import DetailView
from employee.models import Employee


class EmployeeImage(TemplateView):

    form = EmployeeForm
    template_name = 'emp_image.html'

    def post(self, request, *args, **kwargs):

        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():

            print(form.cleaned_data.get('name'))
            im = (form.cleaned_data.get('emp_image'))

            def load_model(im):
                import os
                import numpy as np
                from PIL import Image
                from keras.initializers import glorot_uniform
                import tensorflow as tf
                print("fsdfkdhfjsdhckjxcvzdfjkhvkjxfbgvkjxdv")
                # Reading the model from JSON file
                with open("./resnet50.json", 'r') as json_file:
                    json_savedModel = json_file.read()
                # load the model architecture
                model_j = tf.keras.models.model_from_json(json_savedModel)
                model_j.summary()
                model_j.load_weights("./resnet50.h5")
                # Compiling the model
                model_j.compile(loss='sparse_categorical_crossentropy',
                                optimizer='SGD',
                                metrics=['accuracy'])
                a = im
                read = (lambda x: np.asarray(Image.open(
                    x).convert("RGB").resize((224, 224))))

                im = [read((a))]
                a = np.array(im, dtype='uint8')

                print(np.shape(a))
                y_pred = model_j.predict(a)
                print(1.1, y_pred)

                q = 1
                print(y_pred)
                for i in y_pred:
                    print("%.8f" % i[0])
                    if i[0] > 0.5:
                        return("Benign")
                    else:
                        return(q, "Malignant")
                q += 1

            a = load_model(im)
            html = "<html ><h1> %s.</h1></html>" % a
            return HttpResponse(html)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
