from django.db import models
import uuid, re, __builtin__, os, sys, socket, subprocess, tempfile
from django.db.models.loading import get_model




FieldFactory = lambda base_class, *a1, **kw1: lambda *a2, **kw2: base_class(*(a1 + a2), **(dict(kw1.items() + kw2.items())))
GuidField = FieldFactory(models.CharField, max_length = 36, null = False, blank = False, default = lambda: str(uuid.uuid4()), unique = True, db_index = True)
NameField = FieldFactory(models.CharField, max_length = 255, null = False, blank = False, unique = True, db_index = True)
CaptionField = FieldFactory(models.CharField, max_length = 255, null = False, blank = True, default = '')
ValidationField = FieldFactory(models.CharField, max_length = 255, null = False, blank = False, default = r'\s*(.*)\s*')
C14nField = FieldFactory(models.CharField, max_length = 255, null = False, blank = False, default = r'\1')
DocField = FieldFactory(models.TextField, null = False, blank = True, default = '')

SCOPES = (
    ('host', 'Single host'),
    ('hosts', 'Multiple hosts'),
    ('subnet', 'Subnet'),
    ('cidr', 'Classless Interdomain Routing')
    ('domain', 'Domain name'),
    ('hostname', 'Hostname'),
    ('uri', 'Uniform resource indicator')
)

ADDRESS_FAMILIES = (
    ('ipv4', 'IPv4'),
    ('ipv6', 'IPv6'),
    ('dns', 'DNS'),
)

OUTPUT_MODES = (
    ('pipes', 'Pipe'),
    ('tmpfile', 'Temporary file'),
)

CONTENT_TYPES = (
    ('text/plain', 'Plain text'),
    ('text/html', 'HTML'),
    ('text/xml', 'XML'),
    ('application/xhtml+xml', 'XHTML'),
)

class DBObject(models.Model):
    class Meta: abstract = True

    guid = GuidField()
    name = NameField()
    caption = CaptionField()
    doc = DocField()


class ApiKey(models.Model):
    class Meta: ordering = ['active']

    guid = GuidField()
    created = models.DateTimeField(blank = False, null = False, auto_now_add = True)
    creator = models.ForeignKey('auth.User', blank = False, null = False)
    active = models.BooleanField(blank = False, null = False, default = True)
    scanners = models.ManyToManyField('Scanner')
    
    def __str__(self):
        result = '%s (' % self.guid
        if not self.active: result += 'inactive; '
        result += 'created: %s)' % self.created
        return result
    
class Scanner(DBObject):
    class Meta: ordering = ['name']
    
    command_line = models.CharField(max_length = 255, blank = False, null = False)
    output_mode = models.CharField(max_length = 255, blank = False, null = False, default = 'stdout', choices = OUTPUT_MODES)
    content_type = models.CharField(max_length = 255, blank = False, null = False, default = 'text/plain', choices = CONTENT_TYPES)
    max_duration_seconds = models.IntegerField(blank = False, null = False, default = 900)
    script_template = models.TextField(blank = True, null = True, default = None)
    
    def __str__(self): return self.name
    
class Scan(models.Model):
    class Meta: ordering = ['created', 'started', 'finished']

    guid = GuidField()
    scanner = models.ForeignKey('Scanner')
    target = models.CharField(max_length = 255, blank = False, null = False)
    created = models.DateTimeField(blank = False, null = False, auto_now_add = True)
    started = models.DateTimeField(blank = True, null = True)
    finished = models.DateTimeField(blank = True, null = True)
    output_file = models.CharField(max_length = 255, blank = True, null = True, default = None)
    process_id = models.BigIntegerField(blank = True, null = True, default = None)
    exit_code = models.IntegerField(blank = True, null = True, default = None)
    content_type = models.CharField(max_length = 255, blank = False, null = False, default = 'text/plain', choices = CONTENT_TYPES)
    api_key = ForeignKey('ApiKey')
    
    def is_finished(self): return self.exit_code is not None

    def __str__(self):
        if self.process_id is None: status = 'created: %s' % self.created
        elif self.exit_code is None: status = 'running since: %s' % self.started
        else: status = 'created %s; ran %s - %s; exit code = %d' % (self.created, self.started, self.finished, self.exit_code)
        return '%s - %s' % (self.guid, status)

    def start(self):
        if this.scanner.script_template is not None:
            
        
        subprocess.Popen(