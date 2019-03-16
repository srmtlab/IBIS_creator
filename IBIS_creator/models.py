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
    NODE_TYPES = (
        ('Issue', '課題'),
        ('Idea', 'アイデア'),
        ('Merit', 'メリット'),
        ('Demerit', 'デメリット'),
        ('Example', '例示'),
        ('Reason', '理由'),
        ('Opinion', '意見'),
    )
    node_name = models.TextField()
    node_type = models.CharField(choices=NODE_TYPES, max_length=10)
    node_description = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name="nodes")

    def __str__(self):
        return self.node_name


class RelevantInfo(models.Model):
    # id = models.AutoField(primary_key=True)
    relevant_url = models.URLField()
    relevant_title = models.TextField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="relevant_info")


class NodeNode(models.Model):
    parent_node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, related_name="parent")
    child_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="child")
