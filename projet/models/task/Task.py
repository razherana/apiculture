from django.db import models

class TaskType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'task_types'
        
class TaskPriorite(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'task_priorites'
        
class TaskStatusType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'task_status_type'
        
class Task(models.Model):
    title = models.CharField(max_length=255)
    ruche_id = models.ForeignKey(Ruche, on_delete=models.CASCADE,related_name='tasks')
    localization_id = models.ForeignKey(Localization, on_delete=models.CASCADE,related_name='tasks')
    task_type_id = models.ForeignKey(TaskType, on_delete=models.CASCADE,related_name='tasks')
    description = models.CharField(max_length=255)
    task_priorite_id = models.ForeignKey(TaskPriorite, on_delete=models.CASCADE,related_name='tasks')
    date_prevue = models.DateField()
    date_realisation = models.DateField()
    
    class Meta:
        db_table = 'tasks'
    
    
class TaskStatusHistory(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='task_status_histories')
    task_status_type_id = models.ForeignKey(TaskStatusType, on_delete=models.CASCADE,related_name='task_status_histories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task_status_histories'
  