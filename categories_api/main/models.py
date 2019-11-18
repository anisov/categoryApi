from django.db import models
from django.db.models import QuerySet


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200, unique=True
    )
    parent = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='children',
        on_delete=models.PROTECT
    )

    @property
    def siblings(self):
        if not self.parent_id:
            return []
        return self.convert_qs(
            Category.objects.filter(parent=self.parent_id)
                            .exclude(id=self.pk)
        )

    @staticmethod
    def convert_qs(qs: QuerySet):
        assert not isinstance(qs, Category)
        return list(qs.values('id', 'name',))

    @property
    def children_nodes(self):
        return self.convert_qs(self.children.all())

    def __orm_get_parents(self):
        # Request leak, but orm is used
        obj = self
        parents_list = list()
        while obj.parent:
            obj = obj.parent
            obj_dict = dict(name=obj.name, id=obj.pk)
            parents_list.append(obj_dict)
        return parents_list

    def __row_sql_parents(self):
        # Fast, but use row sql
        query = """
                WITH RECURSIVE CT AS 
                (
                  SELECT * FROM main_category WHERE id=%s
                  UNION ALL
                  SELECT mc.* FROM main_category mc
                     JOIN CT ON mc.id = CT.parent_id
                )
                SELECT id, name FROM CT WHERE id != %s
                """

        parents = self.__class__.objects.raw(
            query, [self.pk, self.pk]
        )
        parents_list = [dict(name=parent.name, id=parent.pk) for parent in parents]

        return parents_list

    @property
    def parents(self):
        # Or can use self.__orm_get_parents()
        return self.__row_sql_parents()

    class Meta:
        verbose_name = "Категрия"
        verbose_name_plural = "Категрии"
