from django import forms
#########################################################    
class dropDownGeneric(forms.Form):
    def __init__(self, *args, **kwargs):
    #   self.label	= kwargs.pop('label')
       self.choices	= kwargs.pop('choices')
       self.tag		= kwargs.pop('tag')
       self.fieldname	= self.tag # 'choice'
       
       super(dropDownGeneric, self).__init__(*args, **kwargs)
       
       self.fields[self.fieldname] = forms.ChoiceField(choices = self.choices, required=False)

    def handleDropSelector(self):
        selection = self.cleaned_data[self.fieldname]
        if(selection=='All' or selection==''):
            return ''
        else:
            return self.tag+'='+selection+'&'

#########################################################
def gtStatusSelector(request, status, gtStatusChoices):
    if request is None:
        return dropDownGeneric(initial={'status':status}, choices=gtStatusChoices, tag='status')
    else:
        return dropDownGeneric(request.POST, initial={'status':status}, choices=gtStatusChoices, tag='status')
