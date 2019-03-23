from django.db import models
# Create your models here.


class Theme(models.Model):
    # id = models.AutoField(primary_key=True)
    theme_name = models.TextField()
    theme_description = models.TextField()

    def __str__(self):
        return self.theme_name

    def dict(self):
        return \
            {
                "theme_id": self.id,
                "theme_name": self.theme_name,
                "theme_description": self.theme_description,
            }


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

    def dict(self):
        return \
            {
                "node_id": self.id,
                "node_name": self.node_name,
                "node_type": self.node_type,
                "node_description": self.node_description,
            }


class RelevantInfo(models.Model):
    # id = models.AutoField(primary_key=True)
    relevant_url = models.URLField()
    relevant_title = models.TextField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="relevant_info")

    def __str__(self):
        return self.relevant_title

    def dict(self):
        return \
            {
                "relevant_info_id": self.id,
                "relevant_info_title": self.relevant_title,
                "relevant_info_url": self.relevant_url,
            }


class NodeNode(models.Model):
    parent_node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, related_name="parent")
    child_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="child")
