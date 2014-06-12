from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ccad.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PhilAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = PhilAddress
		fields = ('city', 'province', 'region', 'regioncode')

class SitenameSerializer(serializers.HyperlinkedModelSerializer):
	#phil_address = serializers.PrimaryKeyRelatedField(required=False)#null=True, source='address', required=False)
	slongitude = serializers.SerializerMethodField("get_longitude")
	slatitude = serializers.SerializerMethodField("get_latitude")
	address = PhilAddressSerializer(required=False)	
	street  = serializers.CharField(source='street', read_only=True) #for testing


	def get_longitude(self, obj):
		if obj.deg_long or obj.min_long or obj.sec_long:
			slongitude = int(obj.deg_long)+int(obj.min_long)/60+int(obj.sec_long)/3600
		if obj.longitude:
			return obj.longitude
		else:
			return slongitude

	def get_latitude(self, obj):
		if obj.deg_lat or obj.min_lat or obj.sec_lat:
			slatitude = int(obj.deg_lat)+int(obj.min_lat)/60+int(obj.sec_lat)/3600
		if obj.latitude:
			return obj.latitude
		else:
			return slatitude

	class Meta:
		model  = Sitename
		fields = ('site', 'street', 'address', 'slatitude', 'slongitude')#, 'site_latitude', 'site_longitude')

class CarrierSerializer(serializers.ModelSerializer):
	class Meta:
		model = Carrier
		fields = ('companyname')

class EquipModlSerializer(serializers.ModelSerializer):
	class Meta:
		model = EquipModel
		fields = ('make',)

class AntennaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Antenna
		fields = ('antenna_type', 'directivity', 'height', 'gain')

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
	freqrange = serializers.SerializerMethodField("get_freqrange")
	txrx      = serializers.SerializerMethodField("get_txrx")
	powerbwe  = serializers.SerializerMethodField("get_powerbwe")
	usagepol  = serializers.SerializerMethodField("get_usagepolarity")
	ant_detail= serializers.SerializerMethodField("get_antenna_details")

	
	def get_freqrange(self, obj):
		if obj.freqrange_low2 or obj.freqrange_high2:
			return u'%s-%s / %s-%s' % (obj.freqrange_low, obj.freqrange_high, obj.freqrange_low2, obj.freqrange_high2)
		else:
			return u'%s-%s' % (obj.freqrange_low, obj.freqrange_high)		

	def get_txrx(self, obj):
		if obj.tx_min or obj.rx_min:
			return u'%s-%s / %s-%s' % (obj.tx_min, obj.tx_max, obj.rx_min, obj.rx_max)
		else:
			return u'%s-%s' % (obj.tx, obj.rx)

	def get_powerbwe(self, obj):
		return u'%s / %s' % (obj.power, obj.bwe)

	def get_usagepolarity(self, obj):
		return u'%s / %s' % (obj.usage, obj.polarity)

	def get_antenna_details(self, obj):		
		return u'Type: %s, Dir: %s, Ht: %s, Gn: %s' % (obj.antenna.antenna_type, obj.antenna.directivity, obj.antenna.height, obj.antenna.gain)
	
	class Meta:
		model = Equipment
		fields = ('id', 'callsign', 'freqrange', 'txrx', 'powerbwe', 'usagepol', 'p_purchase', 'p_possess', 'p_storage', 'ant_detail')

class kpiSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = LogBook
		fields = ('current_user','units', 'noofstation', 'transtype')