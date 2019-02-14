from django.db import models
# Create your models here.


class Theme(models.Model):
    # id = models.AutoField(primary_key=True)
    theme_name = models.TextField()
    theme_description = models.TextField()

    def __str__(self):
        return self.theme_name


class Node(models.Model):
    # id = models.AutoField(primary_key=True)
    node_name = models.TextField()
    node_type = models.CharField(max_length=10)
    node_description = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.node_name


class RelevantInfo(models.Model):
    # id = models.AutoField(primary_key=True)
    relevant_url = models.URLField()
    relevant_title = models.TextField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)


class NodeNode(models.Model):
    parent_node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, related_name="parent_node")
    child_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="child_node")
